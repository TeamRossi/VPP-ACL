/*
*   Flow classification in VPP 
*   (Importing and modifying vamsi's flow table implementation from FAIR DROP)
*
*      acl_flow_table.h
*
*    Version:           2.0
*    Implementation:    Addanki Vamsi Krishna, Valerio Bruschi
*
*/

#ifndef _ACL_FLOW_TABLE_H_
#define _ACL_FLOW_TABLE_H_

#include <vlib/vlib.h>
#include <vnet/ip/ip.h>
#include <vnet/vnet.h>
#include <stdlib.h>
#include <plugins/dpdk/device/dpdk.h>
#include <plugins/dpdk/device/dpdk_priv.h>
#include "hash_lookup_private.h"

#include <vppinfra/crc32.h>
#include <vppinfra/xxhash.h>


#define TABLESIZE 4096
#define NUMFLOWS 10240

#define ACL_FE_CACHE_TIMESHIFT  25
#define ACL_FLOW_CACHE_TTHRESHOLD  0x1000 // = ACL_FLOW_CACHE_TTHRESHOLD * (2^ACL_FE_CACHE_TIMESHIFT / cpu_frequency) [= how many seconds a flow will last] 
// e.g. = 0.012 sec (for 2.6 GHz, cache conf: 25, 0x1)



typedef struct {
  u8 is_valid;
  /* matched ACL */
  u32 acl_index;
  u32 ace_index;
  /*
   * number of hits on this entry
   */
  u64 hitcount;
  /*
   * Action of this applied ACE
   */
  u8 action;
} acl_cache_hash_entry_t;


typedef struct flowcount{
    u32 hash;
    acl_cache_hash_entry_t *entry_pointer;
    struct flowcount * branchnext;
    struct flowcount * update;
}flowcount_t;


extern flowcount_t *  nodet[TABLESIZE];
extern u32 last_hash;

/** Debug counter: number of flows, global hits, global misses **/
extern u64 nflows;
extern u64 ghits;
extern u64 misses;


always_inline u64
compute_hash (fa_5tuple_t * flow)
{
flow->pkt.mask_type_index_lsb = 0;

clib_bihash_kv_40_8_t *v = (clib_bihash_kv_40_8_t *) &flow->kv;
#define VALE_CRC32_HASH
#ifdef VALE_CRC32_HASH
  return clib_crc32c ((u8 *) v->key, 40);
#else
  u64 tmp = v->key[0] ^ v->key[1] ^ v->key[2] ^ v->key[3] ^ v->key[4];
  return clib_xxhash (tmp);
#endif
}




/* Flow classification function */
always_inline flowcount_t *
flow_table_classify(u32 modulox, u32 hashx0){

    flowcount_t * flow;

    if ( (nodet[modulox] + 0) == NULL ){
        nodet[modulox] = malloc(4*sizeof(flowcount_t));
        (nodet[modulox] + 0)->branchnext = NULL;
        (nodet[modulox] + 1)->branchnext = NULL;
        (nodet[modulox] + 2)->branchnext = NULL;
        (nodet[modulox] + 3)->branchnext = NULL;
        nflows++;
        (nodet[modulox] + 0)->hash = hashx0;
        (nodet[modulox] + 0)->update = (nodet[modulox] + 0);
        flow = nodet[modulox] + 0;
	flow->entry_pointer = NULL;
    }

    else if  ((nodet[modulox] + 0)->branchnext == NULL)
    {
        if  ( (nodet[modulox] + 0)->hash != hashx0 )
        {
            nflows++;
            (nodet[modulox] + 1)->hash = hashx0;
            (nodet[modulox] + 0)->branchnext = (nodet[modulox] + 1);
            flow = nodet[modulox] + 1;
	    flow->entry_pointer = NULL;
        }
        else
        {
            flow = nodet[modulox] + 0;
        }
    }

    else if ( (nodet[modulox] + 1)->branchnext == NULL )
    {
        if ( (nodet[modulox] + 0)->hash != hashx0 ) {
            if ( (nodet[modulox] + 1)->hash != hashx0 ) {

                nflows++;
                (nodet[modulox] + 2)->hash = hashx0;
                (nodet[modulox] + 1)->branchnext = nodet[modulox] + 2;
                flow = nodet[modulox] + 2;
		flow->entry_pointer = NULL;
            }
            else
            {
                flow = nodet[modulox] + 1;
            }
        }
        else
        {
            flow = nodet[modulox] + 0;
        }
    }

    else if ( (nodet[modulox] + 2)->branchnext == NULL ){
        if ( (nodet[modulox] + 0)->hash != hashx0 ) {
            if ( (nodet[modulox] + 1)->hash != hashx0 ) {
                if ( (nodet[modulox] + 2)->hash != hashx0 ) {

                    nflows++;
                    (nodet[modulox] + 3)->hash = hashx0;
                    (nodet[modulox] + 2)->branchnext = nodet[modulox] + 3;
                    (nodet[modulox] + 3)->branchnext = nodet[modulox] + 0;
                    flow = nodet[modulox] + 3;
		    flow->entry_pointer = NULL;
                }
                else
                {
                    flow = nodet[modulox] + 2;
                }
            }
            else
            {
                flow = nodet[modulox] + 1;
            }
        }
        else
        {
            flow = nodet[modulox] + 0;
        }
    }

    else
    {
        if ( (nodet[modulox] + 0)->hash != hashx0 ) {

            if ( (nodet[modulox] + 1)->hash != hashx0 ) {

                if ( (nodet[modulox] + 2)->hash != hashx0 ) {

                    if ( (nodet[modulox] + 3)->hash != hashx0 ) {

                        ((nodet[modulox] + 0)->update)->hash = hashx0;
                        flow = (nodet[modulox] + 0)->update;
                        (nodet[modulox] + 0)->update = ((nodet[modulox] + 0)->update)->branchnext ;
                    }
                    else
                    {
                        flow = nodet[modulox] + 3;
                    }
                }
                else
                {
                    flow = nodet[modulox] + 2;
                }
            }
            else
            {
                flow = nodet[modulox] + 1;
            }
        }
        else
        {
            flow = nodet[modulox] + 0;
        }
    }

    return flow;
}




always_inline 
//u8 acl_flow_cache_access (vlib_buffer_t *b0, u32 * acl_index,
u8 acl_flow_cache_access (fa_5tuple_t * flow, u32 * acl_index,
                       u32 * ace_index){

    //struct rte_mbuf *mb0 = (struct rte_mbuf *) rte_mbuf_from_vlib_buffer(b0);
    u32 hash0, modulo0;
    flowcount_t *ft_entry;
    u8 action = ~0;

    //hash0 = mb0->hash.rss;
    hash0 = (u32) compute_hash(flow);
    last_hash = hash0;
    modulo0 = (hash0)%TABLESIZE;
    ft_entry = flow_table_classify(modulo0, hash0);

    acl_cache_hash_entry_t *flow_entry; 
    if (PREDICT_FALSE(ft_entry->entry_pointer == NULL)){
	    //if it consume too much clock cycle is possible to think to pre-allocated a batch of pointers
	    flow_entry = (acl_cache_hash_entry_t *) malloc(sizeof(acl_cache_hash_entry_t));	
	    ft_entry->entry_pointer = flow_entry;
	    flow_entry->hitcount = 0;
	    flow_entry->is_valid = 0;
    }else{
	    flow_entry = (acl_cache_hash_entry_t *) ft_entry->entry_pointer;
    }

    if( flow_entry->is_valid ){
	    *acl_index = flow_entry->acl_index;
	    *ace_index = flow_entry->ace_index;
	    action = flow_entry->action;
	    //vlib_cli_output(&vlib_global_main, "matched flow entry %x (%x) - front end cache, %d %d - action: %d", hash0, modulo0, flow_entry->acl_index, flow_entry->ace_index, action);
	    DBG( "matched flow entry %x (%x) - front end cache, %d %d - action: %d", hash0, modulo0, flow_entry->acl_index, flow_entry->ace_index, action);
	    flow_entry->hitcount = flow_entry->hitcount + 1;
	    ghits++;
    }else{
	    //vlib_cli_output(&vlib_global_main, "not valid - flow entry %x (%x) - front end cache, %d %d - action: %d", hash0, modulo0, flow_entry->acl_index, flow_entry->ace_index, action);
	    misses++;
    }

    return action;
}


always_inline 
//void acl_flow_cache_upload (vlib_buffer_t *b0, u32 acl_index,
void acl_flow_cache_upload (fa_5tuple_t * flow, u32 acl_index,
                       u32 ace_index, u8 action){

    //struct rte_mbuf *mb0 = (struct rte_mbuf *) rte_mbuf_from_vlib_buffer(b0);
    u32 hash0, modulo0;
    flowcount_t * ft_entry;

    //hash0 = mb0->hash.rss;
    //hash0 = (u32) compute_hash(flow);
    hash0 = last_hash;
    modulo0 = (hash0)%TABLESIZE;
    ft_entry = flow_table_classify(modulo0, hash0);

    acl_cache_hash_entry_t *flow_entry; 
    if (PREDICT_FALSE(ft_entry->entry_pointer == NULL)){
	    //if it consume too much clock cycle is possible to think to pre-allocated a batch of pointers
	    flow_entry = (acl_cache_hash_entry_t *) malloc(sizeof(acl_cache_hash_entry_t));	
	    ft_entry->entry_pointer = flow_entry;
    }else{
	    flow_entry = (acl_cache_hash_entry_t *) ft_entry->entry_pointer;
    }

    //vlib_cli_output(&vlib_global_main, "new flow entry - front end cache: %x (%x)", hash0, modulo0);
    DBG( "new flow entry - front end cache: %x (%x)", hash0, modulo0);
    //creare kv_value! vec_entry!
    flow_entry->acl_index =  acl_index;
    flow_entry->ace_index =  ace_index;
    flow_entry->hitcount = 0;
    flow_entry->action = action;
    flow_entry->is_valid = 1;

}


always_inline void
show_acl_frontend_cache (vlib_main_t * vm, u32 is_verbose){ 

	if(is_verbose){
		vlib_cli_output(vm, "|Entry\t|Hash(is_valid) |Hitcount\t|Rule\t\t|Action|"); 
		vlib_cli_output(vm, "|----------------------------------------------------------------------|"); 
		for (int i = 0 ; i < (TABLESIZE -1); i++){
			if ( ((nodet[i] + 0) != NULL) || ((nodet[i] + 1) != NULL) || ((nodet[i] + 2) != NULL) || ((nodet[i] + 3) != NULL) ){
				if ( (nodet[i] + 0) != NULL ){
					acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 0)->entry_pointer;
					vlib_cli_output(vm, "|%3x\t| %8x (%1d)\t| %8ld\t| %4d-%4d\t|%3d|", i, (nodet[i] + 0)->hash, 
							flow_entry->is_valid, flow_entry->hitcount, flow_entry->acl_index, 
							flow_entry->ace_index, flow_entry->action);
					if ( (nodet[i] + 0)->branchnext != NULL ){
						acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 1)->entry_pointer;
						vlib_cli_output(vm, "|\t| %8x (%1d)\t| %8ld\t| %4d-%4d\t|%3d|", (nodet[i] + 1)->hash, 
								flow_entry->is_valid, flow_entry->hitcount, flow_entry->acl_index, 
								flow_entry->ace_index, flow_entry->action);
						if ( (nodet[i] + 1)->branchnext != NULL ){
							acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 2)->entry_pointer;
							vlib_cli_output(vm, "|\t| %8x (%1d)\t| %8ld\t| %4d-%4d\t|%3d|", (nodet[i] + 2)->hash, 
									flow_entry->is_valid, flow_entry->hitcount, flow_entry->acl_index, 
									flow_entry->ace_index, flow_entry->action);
							if ( (nodet[i] + 2)->branchnext != NULL ){
								acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 3)->entry_pointer;
								vlib_cli_output(vm, "|\t| %8x (%1d)\t| %8ld\t| %4d-%4d\t|%3d|", (nodet[i] + 3)->hash, 
										flow_entry->is_valid, flow_entry->hitcount, flow_entry->acl_index, 
										flow_entry->ace_index, flow_entry->action);
							}
						}
					}
				}

			}

		}
		vlib_cli_output(vm, "|----------------------------------------------------------------------|"); 
	}else{
		u64 flows = 0, cflows = 0, lhits = 0, valids = 0;
		for (int i = 0 ; i < (TABLESIZE -1); i++){
			if ( ((nodet[i] + 0) != NULL) || ((nodet[i] + 1) != NULL) || ((nodet[i] + 2) != NULL) || ((nodet[i] + 3) != NULL) ){
				if ( (nodet[i] + 0) != NULL ){
					acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 0)->entry_pointer;
					flows++;
					lhits = lhits + flow_entry->hitcount;
					valids = valids + flow_entry->is_valid;
					if ( (nodet[i] + 0)->branchnext != NULL ){
						acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 1)->entry_pointer;
						flows++;
						cflows++;
						lhits = lhits + flow_entry->hitcount;
						valids = valids + flow_entry->is_valid;
						if ( (nodet[i] + 1)->branchnext != NULL ){
							acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 2)->entry_pointer;
							flows++;
							cflows++;
							lhits = lhits + flow_entry->hitcount;
							valids = valids + flow_entry->is_valid;
							if ( (nodet[i] + 2)->branchnext != NULL ){
								acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 3)->entry_pointer;
								flows++;
								cflows++;
								lhits = lhits + flow_entry->hitcount;
								valids = valids + flow_entry->is_valid;
							}
						}
					}
				}

			}

		}
		vlib_cli_output(vm, "|---------------------------------------------------------------------------------------|"); 
		vlib_cli_output(vm, "| Official\t| Counted (Collided)\t| Valids\t| Hitcount-tot\t| Misses\t|"); 
		vlib_cli_output(vm, "| flows   \t| flows             \t|       \t|             \t|       \t|"); 
		vlib_cli_output(vm, "|---------------------------------------------------------------------------------------|"); 
		vlib_cli_output(vm, "| %8d\t| %8d (%8d)\t|%8d\t|%12ld\t|%12ld\t|", nflows, flows, cflows, valids, ghits, misses) ;
		vlib_cli_output(vm, "|---------------------------------------------------------------------------------------|"); 

	}
}

always_inline void
refresh_acl_frontend_cache(){

	for (int i = 0 ; i < (TABLESIZE -1); i++){
		if ( ((nodet[i] + 0) != NULL) || ((nodet[i] + 1) != NULL) || ((nodet[i] + 2) != NULL) || ((nodet[i] + 3) != NULL) ){
			if ( (nodet[i] + 0) != NULL ){
				acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 0)->entry_pointer;
				flow_entry->is_valid = 0;
				if ( (nodet[i] + 0)->branchnext != NULL ){
					acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 1)->entry_pointer;
					flow_entry->is_valid = 0;
					if ( (nodet[i] + 1)->branchnext != NULL ){
						acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 2)->entry_pointer;
						flow_entry->is_valid = 0;
						if ( (nodet[i] + 2)->branchnext != NULL ){
							acl_cache_hash_entry_t *flow_entry = (acl_cache_hash_entry_t *) (nodet[i] + 3)->entry_pointer;
							flow_entry->is_valid = 0;
						}
					}
				}
			}

		}


	}

	misses = 0;
	ghits = 0;

}

always_inline void
hard_refresh_acl_frontend_cache(){

	for (int i = 0 ; i < (TABLESIZE -1); i++){
		if ( ((nodet[i] + 0) != NULL) || ((nodet[i] + 1) != NULL) || ((nodet[i] + 2) != NULL) || ((nodet[i] + 3) != NULL) ){
			if ( (nodet[i] + 0) != NULL ){
				if ( (nodet[i] + 0)->branchnext != NULL ){
					if ( (nodet[i] + 1)->branchnext != NULL ){
						if ( (nodet[i] + 2)->branchnext != NULL ){
							free((nodet[i] + 3)->entry_pointer);
							free((nodet[i] + 3));
							free((nodet[i] + 3));
							(nodet[i] + 2)->branchnext = NULL;
							nflows--;
						}
						free((nodet[i] + 2)->entry_pointer);
						free((nodet[i] + 2));
						free((nodet[i] + 2));
						(nodet[i] + 1)->branchnext = NULL;
						nflows--;
					}
					free((nodet[i] + 1)->entry_pointer);
					free((nodet[i] + 1));
					free((nodet[i] + 1));
					nflows--;
				}
				free((nodet[i] + 0)->entry_pointer);
				free((nodet[i] + 0));
				free((nodet[i] + 0));
				nflows--;
			}

		}


	}
	misses=0;
}

#endif /*ACL_FLOW_TABLE_H*/

/*
*   "Gather ye rosebuds while ye may"
*                  - Mike Portnoy
*
*   End
*
*/

