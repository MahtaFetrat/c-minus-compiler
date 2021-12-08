import re

GRAMMAR = """1. Program -> Declaration-list $
2. Declaration-list -> Declaration Declaration-list | EPSILON
3. Declaration -> Declaration-initial Declaration-prime
4. Declaration-initial -> Type-specifier ID
5. Declaration-prime -> Fun-declaration-prime | Var-declaration-prime
6. Var-declaration-prime -> ; | [ NUM ] ;
7. Fun-declaration-prime -> ( Params ) Compound-stmt
8. Type-specifier -> int | void
9. Params -> int ID Param-prime Param-list | void
10. Param-list -> , Param Param-list | EPSILON
11. Param -> Declaration-initial Param-prime
12. Param-prime -> [ ] | EPSILON
13. Compound-stmt -> { Declaration-list Statement-list }
14. Statement-list -> Statement Statement-list | EPSILON
15. Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt
16. Expression-stmt -> Expression ; | break ; | ;
17. Selection-stmt -> if ( Expression ) Statement Else-stmt
18. Else-stmt -> endif | else Statement endif
19. Iteration-stmt -> repeat Statement until ( Expression )
20. Return-stmt -> return Return-stmt-prime
21. Return-stmt-prime -> ; | Expression ;
22. Expression -> Simple-expression-zegond | ID B
23. B -> = Expression | [ Expression ] H | Simple-expression-prime
24. H -> = Expression | G D C
25. Simple-expression-zegond -> Additive-expression-zegond C
26. Simple-expression-prime -> Additive-expression-prime C
27. C -> Relop Additive-expression | EPSILON
28. Relop -> < | ==
29. Additive-expression -> Term D
30. Additive-expression-prime -> Term-prime D
31. Additive-expression-zegond -> Term-zegond D
32. D -> Addop Term D | EPSILON
33. Addop -> + | -
34. Term -> Factor G
35. Term-prime -> Factor-prime G
36. Term-zegond -> Factor-zegond G
37. G -> * Factor G | EPSILON
38. Factor -> ( Expression ) | ID Var-call-prime | NUM
39. Var-call-prime -> ( Args ) | Var-prime
40. Var-prime -> [ Expression ] | EPSILON
41. Factor-prime -> ( Args ) | EPSILON
42. Factor-zegond -> ( Expression ) | NUM
43. Args -> Arg-list | EPSILON
44. Arg-list -> Expression Arg-list-prime
45. Arg-list-prime -> , Expression Arg-list-prime | EPSILON"""


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
    rules = []
    for rule in GRAMMAR.splitlines():
        rule = sub_illegal_characters(rule, dollar_sign=dollar_sign, epsilon=epsilon)
        left = get_left_hand_side(rule).strip()
        rights = [right.strip() for right in get_right_hand_sides(rule)]
        rules.append((left, rights))
    return rules


def get_ui_input():
    result = ""
    for left, rights in get_rules(dollar_sign="┤", epsilon="ε"):
        result += "\n".join([f"{left} {right}" for right in rights])
    return result


def get_js_dict():
    rule_dict_format = "\t{{\n\t\tleft: '{left}',\n\t\tright: [{rhs_words}]\n\t}},\n"
    rule_dicts = ""
    for left, rights in get_rules(dollar_sign="\\\\u0000", epsilon="null"):
        for right in rights:
            rhs_words = ", ".join([f"'{word}'" for word in right.split(" ")])
            rhs_words = re.sub("'null'", "null", rhs_words)
            rule_dicts += rule_dict_format.format(left=left, rhs_words=rhs_words)
    return f"[\n{rule_dicts}\n]"


def get_production_rules():
    production_rules = {}
    production_rule_no = 0
    for left, rights in get_rules(dollar_sign="┤", epsilon="ε"):
        production_rules[left] = [
            (production_rule_no + i + 1, right.split(" "))
            for i, right in enumerate(rights)
        ]
        production_rule_no += len(rights)
    return production_rules
