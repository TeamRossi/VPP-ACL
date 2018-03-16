static u32
tm_multi_acl_match_get_applied_ace_index(acl_main_t *am, fa_5tuple_t *match)
{
  clib_bihash_kv_48_8_t kv;
  clib_bihash_kv_48_8_t result;
  fa_5tuple_t *kv_key = (fa_5tuple_t *)kv.key;
  hash_acl_lookup_value_t *result_val = (hash_acl_lookup_value_t *)&result.value;
  u64 *pmatch = (u64 *)match;
  u64 *pmask;
  u64 *pkey;
  int mask_type_index;
  u32 curr_match_index = ~0;


//Added by Valerio
#ifdef VALE_ELOG_ACL

  u32 count_loop=0; 
  u8 flags=0; 
  u8 flagr=0;

#endif


  u32 sw_if_index = match->pkt.sw_if_index;
  u8 is_input = match->pkt.is_input;
  applied_hash_ace_entry_t **applied_hash_aces = get_applied_hash_aces(am, is_input, sw_if_index);
  applied_hash_acl_info_t **applied_hash_acls = is_input ? &am->input_applied_hash_acl_info_by_sw_if_index :
                                                    &am->output_applied_hash_acl_info_by_sw_if_index;

  DBG("TRYING TO MATCH: %016llx %016llx %016llx %016llx %016llx %016llx",
	       pmatch[0], pmatch[1], pmatch[2], pmatch[3], pmatch[4], pmatch[5]);

  for(mask_type_index=0; mask_type_index < pool_len(am->ace_mask_type_pool); mask_type_index++) {
    if (!clib_bitmap_get(vec_elt_at_index((*applied_hash_acls), sw_if_index)->mask_type_index_bitmap, mask_type_index)) {
      /* This bit is not set. Avoid trying to match */
      continue;
    }
    ace_mask_type_entry_t *mte = vec_elt_at_index(am->ace_mask_type_pool, mask_type_index);
    pmatch = (u64 *)match;
    pmask = (u64 *)&mte->mask;
    pkey = (u64 *)kv.key;
    /*
    * unrolling the below loop results in a noticeable performance increase.
    int i;
    for(i=0; i<6; i++) {
      kv.key[i] = pmatch[i] & pmask[i];
    }
    */

    *pkey++ = *pmatch++ & *pmask++;
    *pkey++ = *pmatch++ & *pmask++;
    *pkey++ = *pmatch++ & *pmask++;
    *pkey++ = *pmatch++ & *pmask++;
    *pkey++ = *pmatch++ & *pmask++;
    *pkey++ = *pmatch++ & *pmask++;

//Added by Valerio
#ifdef VALE_ELOG_ACL
  count_loop++; 
#endif

    kv_key->pkt.mask_type_index_lsb = mask_type_index;
    DBG("        KEY %3d: %016llx %016llx %016llx %016llx %016llx %016llx", mask_type_index,
		kv.key[0], kv.key[1], kv.key[2], kv.key[3], kv.key[4], kv.key[5]);
    int res = BV (clib_bihash_search) (&am->acl_lookup_hash, &kv, &result);
    if (res == 0) {
      DBG("ACL-MATCH! result_val: %016llx", result_val->as_u64);
      if (result_val->applied_entry_index < curr_match_index) {
	      //check collisions
	      u32 curr_index = result_val->applied_entry_index;
	      applied_hash_ace_entry_t *pae = vec_elt_at_index((*applied_hash_aces),curr_index);
	      hash_acl_info_t *ha = vec_elt_at_index(am->hash_acl_infos, pae->acl_index);
	      u64 collisions = pae->collision + 1;
	      vlib_main_t *vm = &vlib_global_main;
	      vlib_cli_output(vm, "TM-match: %d %d", curr_index, collisions);
	      int i=0;
	      for(i=0; i < collisions; i++){
		      vlib_cli_output(vm, "TM-iMatch: %d", curr_index);
		      pae = vec_elt_at_index((*applied_hash_aces),curr_index);

		      clib_bihash_kv_48_8_t base_key;
		      fa_5tuple_t *base_kv_key = (fa_5tuple_t *) base_key.key;
		      //CHECK MATCH !!
		      hash_ace_info_t *ace_info = vec_elt_at_index(ha->rules, pae->hash_ace_info_index);
		      mte = vec_elt_at_index(am->ace_mask_type_pool, ace_info->base_mask_type_index);
		      pmatch = (u64 *)match;
		      pmask = (u64 *)&mte->mask;
		      pkey = (u64 *)kv.key;

		      *pkey++ = *pmatch++ & *pmask++;
		      *pkey++ = *pmatch++ & *pmask++;
		      *pkey++ = *pmatch++ & *pmask++;
		      *pkey++ = *pmatch++ & *pmask++;
		      *pkey++ = *pmatch++ & *pmask++;
		      *pkey++ = *pmatch++ & *pmask++;


		      kv_key->pkt.mask_type_index_lsb = ace_info->base_mask_type_index;
		      base_kv_key->pkt.mask_type_index_lsb = ace_info->base_mask_type_index;

		      fill_applied_hash_ace_kv(am, applied_hash_aces, sw_if_index, is_input, curr_index, &base_key);
		      print_mask((fa_5tuple_t *)kv.key);
		      print_mask((fa_5tuple_t *)base_key.key);
		      //CHECK MATCH !!
		      int check = memcmp(&kv.key, &base_key.key, sizeof(fa_5tuple_t));
		      vlib_cli_output(vm, "TM-check: %d", check);
		      //if(!(memcmp(&kv.key, &base_key.key, sizeof(fa_5tuple_t)) == 0)){ 
		      if(!(check == 0)){ 
			      curr_index = pae->next_applied_entry_index;
			      continue;
		      }

		      if (PREDICT_FALSE(result_val->need_portrange_check)) {
			      /*
			       * This is going to be slow, since we can have multiple superset
			       * entries for narrow-ish portranges, e.g.:
			       * 0..42 100..400, 230..60000,
			       * so we need to walk linearly and check if they match.
			       */

			      //Added by Valerio
#ifdef VALE_ELOG_ACL
			      flagr = 0xFF;
			      count_loop++; 
#endif
			      match_portranges(am, match, curr_index);
			      /*
				 u32 curr_index = result_val->applied_entry_index;
				 while ((curr_index != ~0) && !match_portranges(am, match, curr_index)) {
			      // while no match and there are more entries, walk... 

			      applied_hash_ace_entry_t *pae = vec_elt_at_index((*applied_hash_aces),curr_index);
			      DBG("entry %d did not portmatch, advancing to %d", curr_index, pae->next_applied_entry_index);
			      curr_index = pae->next_applied_entry_index;
			      }
			       */
			      if (curr_index < curr_match_index) {
				      DBG("The index %d is the new candidate in portrange matches.", curr_index);
				      curr_match_index = curr_index;
			      } else {
				      DBG("Curr portmatch index %d is too big vs. current matched one %d", curr_index, curr_match_index);
			      }
		      } else {
			      /* The usual path is here. Found an entry in front of the current candiate - so it's a new one */
			      DBG("This match is the new candidate");
			      curr_match_index = result_val->applied_entry_index;
			      if (!result_val->shadowed) {
				      /* new result is known to not be shadowed, so no point to look up further */

				      //Added by Valerio
#ifdef VALE_ELOG_ACL

				      flags=0xFF; 

#endif
				      break;
			      }
		      }
		      DBG("entry %d did not portmatch, advancing to %d", curr_index, pae->next_applied_entry_index);
		      curr_index = pae->next_applied_entry_index;
	      }
          }
      }
    }

  //Added by Valerio
#ifdef VALE_ELOG_ACL
  /*Log event*/
  vlib_main_t *vm = &vlib_global_main;
  // Replace and/or change with u32 Vector Size inside the stuct. Also change the %ll
  ELOG_TYPE_DECLARE (e) = {
	  .format = "ACE: %d, CountLoop = %d, FlagS: %d Flagr: %d",
	  .format_args = "i4i4i1i1",
  };
  struct {u32 ace_i; u32 count_loop; u8 flags; u8 flagr;} *ed;
  ed = ELOG_DATA (&vm->elog_main, e);
  ed->ace_i = curr_match_index;
  ed->count_loop = count_loop;
  ed->flags = flags;
  ed->flagr = flagr;

  /*End of Log event*/

#endif


  DBG("MATCH-RESULT: %d", curr_match_index);
  return curr_match_index;
}



u32
tm_multi_acl_match_get_applied_ace_index(acl_main_t *am, fa_5tuple_t *match)
{
  clib_bihash_kv_48_8_t kv;
  clib_bihash_kv_48_8_t result;
  fa_5tuple_t *kv_key = (fa_5tuple_t *)kv.key;
  hash_acl_lookup_value_t *result_val = (hash_acl_lookup_value_t *)&result.value;
  u64 *pmatch = (u64 *)match;
  u64 *pmask;
  u64 *pkey;
  int mask_type_index;
  u32 curr_match_index = ~0;


//Added by Valerio
#ifdef VALE_ELOG_ACL

  u32 count_loop=0; 
  u8 flags=0; 
  u8 flagr=0;

#endif


  u32 sw_if_index = match->pkt.sw_if_index;
  u8 is_input = match->pkt.is_input;
  applied_hash_ace_entry_t **applied_hash_aces = get_applied_hash_aces(am, is_input, sw_if_index);
  applied_hash_acl_info_t **applied_hash_acls = is_input ? &am->input_applied_hash_acl_info_by_sw_if_index :
                                                    &am->output_applied_hash_acl_info_by_sw_if_index;

  DBG("TRYING TO MATCH: %016llx %016llx %016llx %016llx %016llx %016llx",
	       pmatch[0], pmatch[1], pmatch[2], pmatch[3], pmatch[4], pmatch[5]);

  for(mask_type_index=0; mask_type_index < pool_len(am->ace_mask_type_pool); mask_type_index++) {
    if (!clib_bitmap_get(vec_elt_at_index((*applied_hash_acls), sw_if_index)->mask_type_index_bitmap, mask_type_index)) {
      /* This bit is not set. Avoid trying to match */
      continue;
    }
    ace_mask_type_entry_t *mte = vec_elt_at_index(am->ace_mask_type_pool, mask_type_index);
    pmatch = (u64 *)match;
    pmask = (u64 *)&mte->mask;
    pkey = (u64 *)kv.key;
    /*
    * unrolling the below loop results in a noticeable performance increase.
    int i;
    for(i=0; i<6; i++) {
      kv.key[i] = pmatch[i] & pmask[i];
    }
    */

    *pkey++ = *pmatch++ & *pmask++;
    *pkey++ = *pmatch++ & *pmask++;
    *pkey++ = *pmatch++ & *pmask++;
    *pkey++ = *pmatch++ & *pmask++;
    *pkey++ = *pmatch++ & *pmask++;
    *pkey++ = *pmatch++ & *pmask++;

//Added by Valerio
#ifdef VALE_ELOG_ACL
  count_loop++; 
#endif

    kv_key->pkt.mask_type_index_lsb = mask_type_index;
    DBG("        KEY %3d: %016llx %016llx %016llx %016llx %016llx %016llx", mask_type_index,
		kv.key[0], kv.key[1], kv.key[2], kv.key[3], kv.key[4], kv.key[5]);
    int res = BV (clib_bihash_search) (&am->acl_lookup_hash, &kv, &result);
    if (res == 0) {
      DBG("ACL-MATCH! result_val: %016llx", result_val->as_u64);
      if (result_val->applied_entry_index < curr_match_index) {
	      //check collisions
	      u32 curr_index = result_val->applied_entry_index;
	      applied_hash_ace_entry_t *pae = vec_elt_at_index((*applied_hash_aces),curr_index);
	      u32 last_index = pae->tail_applied_entry_index;
	      while(curr_index != last_index){
		      pae = vec_elt_at_index((*applied_hash_aces),curr_index);

		      clib_bihash_kv_48_8_t base_key;
		      fa_5tuple_t *kv_key = (fa_5tuple_t *) base_key.key;
		      //CHECK MATCH !!
		      mte = vec_elt_at_index(am->ace_mask_type_pool, base_mask_type_index);
		      pmatch = (u64 *)match;
		      pmask = (u64 *)&mte->mask;
		      pkey = (u64 *)kv.key;

		      *pkey++ = *pmatch++ & *pmask++;
		      *pkey++ = *pmatch++ & *pmask++;
		      *pkey++ = *pmatch++ & *pmask++;
		      *pkey++ = *pmatch++ & *pmask++;
		      *pkey++ = *pmatch++ & *pmask++;
		      *pkey++ = *pmatch++ & *pmask++;


		      kv_key->pkt.mask_type_index_lsb = base_mask_type_index;

		      fill_applied_hash_ace_kv(am, applied_hash_aces, sw_if_index, is_input, curr_index, &base_key);
		      //CHECK MATCH !!
		      if(!(memcmp(pkey, base_key, sizeof(kv_key)) == 0)){ 
			      curr_index = pae->next_applied_entry_index;
			      continue;
		      }

		      if (PREDICT_FALSE(result_val->need_portrange_check)) {
			      /*
			       * This is going to be slow, since we can have multiple superset
			       * entries for narrow-ish portranges, e.g.:
			       * 0..42 100..400, 230..60000,
			       * so we need to walk linearly and check if they match.
			       */

			      //Added by Valerio
#ifdef VALE_ELOG_ACL
			      flagr = 0xFF;
			      count_loop++; 
#endif
			      match_portranges(am, match, curr_index);
			      /*
				 u32 curr_index = result_val->applied_entry_index;
				 while ((curr_index != ~0) && !match_portranges(am, match, curr_index)) {
			      // while no match and there are more entries, walk... 

			      applied_hash_ace_entry_t *pae = vec_elt_at_index((*applied_hash_aces),curr_index);
			      DBG("entry %d did not portmatch, advancing to %d", curr_index, pae->next_applied_entry_index);
			      curr_index = pae->next_applied_entry_index;
			      }
			       */
			      if (curr_index < curr_match_index) {
				      DBG("The index %d is the new candidate in portrange matches.", curr_index);
				      curr_match_index = curr_index;
			      } else {
				      DBG("Curr portmatch index %d is too big vs. current matched one %d", curr_index, curr_match_index);
			      }
		      } else {
			      /* The usual path is here. Found an entry in front of the current candiate - so it's a new one */
			      DBG("This match is the new candidate");
			      curr_match_index = result_val->applied_entry_index;
			      if (!result_val->shadowed) {
				      /* new result is known to not be shadowed, so no point to look up further */

				      //Added by Valerio
#ifdef VALE_ELOG_ACL

				      flags=0xFF; 

#endif
				      break;
			      }
		      }
		      DBG("entry %d did not portmatch, advancing to %d", curr_index, pae->next_applied_entry_index);
		      curr_index = pae->next_applied_entry_index;
	      }
          }
      }
    }

  //Added by Valerio
#ifdef VALE_ELOG_ACL
  /*Log event*/
  vlib_main_t *vm = &vlib_global_main;
  // Replace and/or change with u32 Vector Size inside the stuct. Also change the %ll
  ELOG_TYPE_DECLARE (e) = {
	  .format = "ACE: %d, CountLoop = %d, FlagS: %d Flagr: %d",
	  .format_args = "i4i4i1i1",
  };
  struct {u32 ace_i; u32 count_loop; u8 flags; u8 flagr;} *ed;
  ed = ELOG_DATA (&vm->elog_main, e);
  ed->ace_i = curr_match_index;
  ed->count_loop = count_loop;
  ed->flags = flags;
  ed->flagr = flagr;

  /*End of Log event*/

#endif


  DBG("MATCH-RESULT: %d", curr_match_index);
  return curr_match_index;
}


