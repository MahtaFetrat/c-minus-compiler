import re
from pprint import pprint

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


def get_ui_input():
    converted_grammar = ""
    for rule in GRAMMAR.splitlines():
        rule = re.sub(r"\$", "┤", rule)
        rule = re.sub("EPSILON", "ε", rule)
        rule = re.sub(r"([^-]*\w)-(\w[^-])", r"\1_\2", rule)
        rule = re.sub(r"[0-9]+\. ", "", rule)
        left = re.search(r"(.*)->", rule).group(1)
        rights = re.search(r".*->(.*)", rule).group(1).split("|")
        for r in rights:
            converted_grammar += left + r + "\n"
        return converted_grammar


def get_js_dict():
    rule_dicts = "[\n"
    for rule in GRAMMAR.splitlines():
        rule = re.sub(r"\$", "\\\\u0000", rule)
        rule = re.sub("EPSILON", "null", rule)
        rule = re.sub(r"([^-]*\w)-(\w[^-])", r"\1_\2", rule)
        rule = re.sub(r"[0-9]+\. ", "", rule)
        left = re.search(r"(.*)->", rule).group(1)
        rights = re.search(r".*->(.*)", rule).group(1).split("|")
        for r in rights:
            r = r.strip()
            rule_dict = "\t{\n\t\tleft: '" + left.strip() + "',\n\t\tright: ["
            for r_part in r.split(" "):
                rule_dict += "'" + r_part + "'," if r_part != "null" else r_part
            rule_dict += "]\n\t},\n"
            rule_dicts += rule_dict
    rule_dicts += "]\n"
    return rule_dicts


def get_production_rules():
    production_rules = {}
    production_rules_no = 0
    for rule in GRAMMAR.splitlines():
        rule = re.sub(r"\$", "┤", rule)
        rule = re.sub("EPSILON", "ε", rule)
        rule = re.sub(r"([^-]*\w)-(\w[^-])", r"\1_\2", rule)
        rule = re.sub(r"[0-9]+\. ", "", rule)
        left = re.search(r"(.*)->", rule).group(1)
        rights = re.search(r".*->(.*)", rule).group(1).split("|")
        production_rules[left.strip()] = (
            left.strip(),
            [
                (
                    production_rules_no + production_rule_no + 1,
                    right.strip().split(" "),
                )
                for production_rule_no, right in enumerate(rights)
            ],
        )
        production_rules_no += len(rights)
    return production_rules
