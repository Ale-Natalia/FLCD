%{
#include <stdio.h>
extern FILE *yyin;
extern char *yytext;
extern int yylineno;
%}

%token let const if then else while read len sin print
%token BOOLEAN CHAR STRING INTEGER FLOAT
%token id constant

%token op_plus op_minus op_mul op_div op_eq op_gte op_lte op_gt op_lt op_or op_and op_mod op_eqeq op_dif op_pluseq op_minuseq op_muleq op_diveq op_modeq op_andeq op_oreq
%token sep_open_par sep_closed_par sep_open_br sep_closed_br sep_open_curl sep_closed_curl sep_col sep_semicol sep_com

%%
program: decllist sep_semicol cmpdstmt
		;
decllist: declaration decllist_rest
        ;
decllist_rest: /*epsilon*/
        | sep_semicol decllist
		;
declaration: decl_keyword id declaration_rest
        ;
declaration_rest: sep_semicol
        | op_eq expression sep_semicol
        ;
decl_keyword: let 
        | const
        ;
maintype: BOOLEAN
        | CHAR
        | STRING
        | INTEGER
        | FLOAT
        ;
arraydecl: sep_open_br maintype sep_closed_br sep_open_par INTEGER sep_closed_par
        | array_val
        ;
array_val: sep_open_br array_terms sep_closed_br
        ;
array_terms: term array_terms_rest 
        ;
array_terms_rest: /*epsilon*/
        | sep_com array_terms
        ;
type: maintype
        | arraydecl
        ;
cmpdstmt: stmtlist
        ;
stmtlist: stmt sep_semicol stmtlist_rest
        ;
stmtlist_rest: /*epsilon*/
        | stmtlist
        ;
stmt: simplstmt 
        | structstmt
        ;
simplstmt: assignstmt 
        | iostmt
        ;
assignstmt: id assignstmt_rest
        ;
assignstmt_rest: op_eq expression
        | arith_assign_sign arith_expression
        | op_pluseq str_expression
        | bool_assign_sign bool_expression
        ;
arith_assign_sign: op_pluseq 
        | op_minuseq 
        | op_muleq 
        | op_diveq 
        | op_modeq
        ;
bool_assign_sign: op_oreq 
        | op_andeq
        ;
expression: arith_expression 
        | str_expression 
        | bool_expression
        ;
term: arith_term 
        | bool_term 
        | str_term
        ;
arith_expression: arith_term arith_expression_rest
        ;
arith_expression_rest: /*epsilon*/
        | arith_op arith_expression
        ;
arith_term: INTEGER 
        | FLOAT
        | factor
        ;
arith_op: op_mul
        | op_plus
        | op_minus
        | op_div
        | op_mod
        ;
str_expression: STRING str_expression_rest
        ;
str_expression_rest: /*epsilon*/
        | str_op str_term
        ;
str_term: STRING
        ;
str_op: op_plus
        ;
bool_expression: bool_term bool_expression_rest
        ;
bool_expression_rest: /*eps*/
        | bool_op bool_expression
        ;
bool_term: BOOLEAN
        ;
bool_op: op_and
        | op_or
        ;
factor: sep_open_par expression sep_closed_par
        | id
        ;
iostmt: read sep_open_par id sep_closed_par
        | print sep_open_par id sep_closed_par
        ;
structstmt: cmpdstmt 
        | ifstmt 
        | whilestmt
        ;
ifstmt: if condition then sep_open_curl stmt sep_closed_curl ifstmt_rest        ;
ifstmt_rest: /*epsilon*/
        | else sep_open_curl stmt sep_closed_curl
        ;
whilestmt: while condition sep_open_curl stmt sep_closed_curl
condition: expression relation expression
relation: op_lt 
        | op_lte
        | op_eq
        | op_dif
        | op_gt
        | op_gte
        ;

%%
int main(int argc, char **argv)
{
	if (argc == 2) {
		yyin = fopen(argv[1], "r");
		yyparse();
	}
	else{
		printf("No input file given!\n");
	}
  	if(0==yyparse()) printf("Result yyparse OK");
}

int yyerror(char *s)
{
    printf("Error on line #%d\n", yylineno);
    printf("Unexpected token: '%s'\n", yytext);
    return 0;
}
