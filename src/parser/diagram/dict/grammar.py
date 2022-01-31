import re

GRAMMAR = """1. Program -> Declaration-list $
2. Declaration-list -> Declaration Declaration-list | EPSILON
3. Declaration -> #declare Declaration-initial Declaration-prime
4. Declaration-initial -> #declare_type Type-specifier #declare_ID ID
5. Declaration-prime -> # save #declare_func #add_scope Fun-declaration-prime #release_scope #skip | Var-declaration-prime
6. Var-declaration-prime -> #declare_var ; | #declare_array [ #cell_no NUM ] ;
7. Fun-declaration-prime -> ( Params ) #save #set_call_address Compound-stmt #set_runtime_stack_top #return_jp
8. Type-specifier -> int | void
9. Params -> #declare #arg_count #declare_type int #declare_ID ID Param-prime Param-list | void
10. Param-list -> , Param Param-list | EPSILON
11. Param -> #declare #arg_count Declaration-initial Param-prime
12. Param-prime -> #declare_array [ ] | #declare_var EPSILON
13. Compound-stmt -> { Declaration-list Statement-list }
14. Statement-list -> Statement Statement-list | EPSILON
15. Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt
16. Expression-stmt -> #stmt_flag Expression #pop_stmt_flag ; | break  #break_jp ; | ;
17. Selection-stmt -> if ( Expression ) #save Statement Else-stmt
18. Else-stmt -> endif #jpf | else #jpf_save Statement #jp endif
19. Iteration-stmt -> repeat #break_label #save #label Statement until ( Expression ) #repeat #break_assign
20. Return-stmt -> return Return-stmt-prime
21. Return-stmt-prime -> ; | Expression ;
22. Expression -> Simple-expression-zegond | #pid ID B
23. B -> #assign_id = Expression #assign | #assign_id [ Expression #displace ] H | #apply_id  Simple-expression-prime
24. H -> = Expression #assign | #get_indirect_value G D C
25. Simple-expression-zegond -> Additive-expression-zegond C
26. Simple-expression-prime -> Additive-expression-prime C
27. C -> #relop Relop Additive-expression #cmp | EPSILON
28. Relop -> < | ==
29. Additive-expression -> Term D
30. Additive-expression-prime -> Term-prime D
31. Additive-expression-zegond -> Term-zegond D
32. D -> #addop Addop Term #add D | EPSILON
33. Addop -> + | -
34. Term -> Factor G
35. Term-prime -> Factor-prime G
36. Term-zegond -> Factor-zegond G
37. G -> * Factor #mult G | EPSILON
38. Factor -> ( Expression ) | #pid ID Var-call-prime | #pnum NUM
39. Var-call-prime -> #update_displays #reset_arg_no ( Args ) #func_call | Var-prime
40. Var-prime ->  #assign_id [ Expression #displace ] #get_indirect_value | #apply_id EPSILON
41. Factor-prime -> #get_runtime_mem ( Args ) #func_call | EPSILON
42. Factor-zegond -> ( Expression ) | #pnum NUM
43. Args -> Arg-list | EPSILON
44. Arg-list -> Expression #set_arg Arg-list-prime
45. Arg-list-prime -> , Expression #set_arg Arg-list-prime | EPSILON"""


def sub_illegal_characters(rule, dollar_sign, epsilon):
    rule = re.sub(r"\$", dollar_sign, rule)
    rule = re.sub("EPSILON", epsilon, rule)
    rule = re.sub(r"([^-]*\w)-(\w[^-])", r"\1_\2", rule)
    rule = re.sub(r"[0-9]+\. ", "", rule)
    return rule


def get_left_hand_side(rule):
    return re.search(r"(.*)->", rule).group(1)


def get_right_hand_sides(rule):
    return re.search(r".*->(.*)", rule).group(1).split("|")


def get_rules(dollar_sign, epsilon):
    """Returns the grammar in tuples of lhs and rhs rules.
    special characters (i.e. $ and epsilon) are converted to the desired char."""
    rules = []
    for rule in GRAMMAR.splitlines():
        rule = sub_illegal_characters(rule, dollar_sign=dollar_sign, epsilon=epsilon)
        left = get_left_hand_side(rule).strip()
        rights = [right.strip() for right in get_right_hand_sides(rule)]
        rules.append((left, rights))
    return rules


def get_ui_input():
    """Get valid input for https://mikedevice.github.io/first-follow/ GUI input."""
    result = ""
    for left, rights in get_rules(dollar_sign="┤", epsilon="ε"):
        result += "\n".join([f"{left} {right}" for right in rights])
    return result


def get_js_dict():
    """Get valid input for https://mikedevice.github.io/first-follow/ code input."""
    rule_dict_format = "\t{{\n\t\tleft: '{left}',\n\t\tright: [{rhs_words}]\n\t}},\n"
    rule_dicts = ""
    for left, rights in get_rules(dollar_sign="\\\\u0000", epsilon="null"):
        for right in rights:
            rhs_words = ", ".join([f"'{word}'" for word in right.split(" ")])
            rhs_words = re.sub("'null'", "null", rhs_words)
            rule_dicts += rule_dict_format.format(left=left, rhs_words=rhs_words)
    return f"[\n{rule_dicts}\n]"


def get_production_rules():
    """Get a dict of rule_names to their enumerated production_rules.
    Every production rule is returned as a list of its space-separated terminals and non-terminals."""
    production_rules = {}
    production_rule_no = 0
    for left, rights in get_rules(dollar_sign="┤", epsilon="ε"):
        production_rules[left] = [
            (production_rule_no + i + 1, right.split(" "))
            for i, right in enumerate(rights)
        ]
        production_rule_no += len(rights)
    return production_rules
