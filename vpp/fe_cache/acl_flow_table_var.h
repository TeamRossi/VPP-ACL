#ifndef _ACL_FLOW_TABLE_VAR_H_
#define _ACL_FLOW_TABLE_VAR_H_

#include <plugins/acl/acl_flow_table.h>
flowcount_t *  nodet[TABLESIZE] ;
u32 last_hash;
u64 nflows=0;
u64 ghits=0;
u64 expired=0;
u64 misses=0;

#endif
