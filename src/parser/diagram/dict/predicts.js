const firstFollow = require('first-follow');

const rules = [
	{
		left: 'Program',
		right: ['Declaration_list','\u0000',]
	},
	{
		left: 'Declaration_list',
		right: ['Declaration','Declaration_list',]
	},
	{
		left: 'Declaration_list',
		right: [null]
	},
	{
		left: 'Declaration',
		right: ['Declaration_initial','Declaration_prime',]
	},
	{
		left: 'Declaration_initial',
		right: ['Type_specifier','ID',]
	},
	{
		left: 'Declaration_prime',
		right: ['Fun_declaration_prime',]
	},
	{
		left: 'Declaration_prime',
		right: ['Var_declaration_prime',]
	},
	{
		left: 'Var_declaration_prime',
		right: [';',]
	},
	{
		left: 'Var_declaration_prime',
		right: ['[','NUM',']',';',]
	},
	{
		left: 'Fun_declaration_prime',
		right: ['(','Params',')','Compound_stmt',]
	},
	{
		left: 'Type_specifier',
		right: ['int',]
	},
	{
		left: 'Type_specifier',
		right: ['void',]
	},
	{
		left: 'Params',
		right: ['int','ID','Param_prime','Param_list',]
	},
	{
		left: 'Params',
		right: ['void',]
	},
	{
		left: 'Param_list',
		right: [',','Param','Param_list',]
	},
	{
		left: 'Param_list',
		right: [null]
	},
	{
		left: 'Param',
		right: ['Declaration_initial','Param_prime',]
	},
	{
		left: 'Param_prime',
		right: ['[',']',]
	},
	{
		left: 'Param_prime',
		right: [null]
	},
	{
		left: 'Compound_stmt',
		right: ['{','Declaration_list','Statement_list','}',]
	},
	{
		left: 'Statement_list',
		right: ['Statement','Statement_list',]
	},
	{
		left: 'Statement_list',
		right: [null]
	},
	{
		left: 'Statement',
		right: ['Expression_stmt',]
	},
	{
		left: 'Statement',
		right: ['Compound_stmt',]
	},
	{
		left: 'Statement',
		right: ['Selection_stmt',]
	},
	{
		left: 'Statement',
		right: ['Iteration_stmt',]
	},
	{
		left: 'Statement',
		right: ['Return_stmt',]
	},
	{
		left: 'Expression_stmt',
		right: ['Expression',';',]
	},
	{
		left: 'Expression_stmt',
		right: ['break',';',]
	},
	{
		left: 'Expression_stmt',
		right: [';',]
	},
	{
		left: 'Selection_stmt',
		right: ['if','(','Expression',')','Statement','Else_stmt',]
	},
	{
		left: 'Else_stmt',
		right: ['endif',]
	},
	{
		left: 'Else_stmt',
		right: ['else','Statement','endif',]
	},
	{
		left: 'Iteration_stmt',
		right: ['repeat','Statement','until','(','Expression',')',]
	},
	{
		left: 'Return_stmt',
		right: ['return','Return_stmt_prime',]
	},
	{
		left: 'Return_stmt_prime',
		right: [';',]
	},
	{
		left: 'Return_stmt_prime',
		right: ['Expression',';',]
	},
	{
		left: 'Expression',
		right: ['Simple_expression_zegond',]
	},
	{
		left: 'Expression',
		right: ['ID','B',]
	},
	{
		left: 'B',
		right: ['=','Expression',]
	},
	{
		left: 'B',
		right: ['[','Expression',']','H',]
	},
	{
		left: 'B',
		right: ['Simple_expression_prime',]
	},
	{
		left: 'H',
		right: ['=','Expression',]
	},
	{
		left: 'H',
		right: ['G','D','C',]
	},
	{
		left: 'Simple_expression_zegond',
		right: ['Additive_expression_zegond','C',]
	},
	{
		left: 'Simple_expression_prime',
		right: ['Additive_expression_prime','C',]
	},
	{
		left: 'C',
		right: ['Relop','Additive_expression',]
	},
	{
		left: 'C',
		right: [null]
	},
	{
		left: 'Relop',
		right: ['<',]
	},
	{
		left: 'Relop',
		right: ['==',]
	},
	{
		left: 'Additive_expression',
		right: ['Term','D',]
	},
	{
		left: 'Additive_expression_prime',
		right: ['Term_prime','D',]
	},
	{
		left: 'Additive_expression_zegond',
		right: ['Term_zegond','D',]
	},
	{
		left: 'D',
		right: ['Addop','Term','D',]
	},
	{
		left: 'D',
		right: [null]
	},
	{
		left: 'Addop',
		right: ['+',]
	},
	{
		left: 'Addop',
		right: ['-',]
	},
	{
		left: 'Term',
		right: ['Factor','G',]
	},
	{
		left: 'Term_prime',
		right: ['Factor_prime','G',]
	},
	{
		left: 'Term_zegond',
		right: ['Factor_zegond','G',]
	},
	{
		left: 'G',
		right: ['*','Factor','G',]
	},
	{
		left: 'G',
		right: [null]
	},
	{
		left: 'Factor',
		right: ['(','Expression',')',]
	},
	{
		left: 'Factor',
		right: ['ID','Var_call_prime',]
	},
	{
		left: 'Factor',
		right: ['NUM',]
	},
	{
		left: 'Var_call_prime',
		right: ['(','Args',')',]
	},
	{
		left: 'Var_call_prime',
		right: ['Var_prime',]
	},
	{
		left: 'Var_prime',
		right: ['[','Expression',']',]
	},
	{
		left: 'Var_prime',
		right: [null]
	},
	{
		left: 'Factor_prime',
		right: ['(','Args',')',]
	},
	{
		left: 'Factor_prime',
		right: [null]
	},
	{
		left: 'Factor_zegond',
		right: ['(','Expression',')',]
	},
	{
		left: 'Factor_zegond',
		right: ['NUM',]
	},
	{
		left: 'Args',
		right: ['Arg_list',]
	},
	{
		left: 'Args',
		right: [null]
	},
	{
		left: 'Arg_list',
		right: ['Expression','Arg_list_prime',]
	},
	{
		left: 'Arg_list_prime',
		right: [',','Expression','Arg_list_prime',]
	},
	{
		left: 'Arg_list_prime',
		right: [null]
	},
]

const { firstSets, followSets, predictSets } = firstFollow(rules);

console.log(JSON.stringify(firstSets));

console.log(JSON.stringify(followSets));

console.log(JSON.stringify(predictSets));
