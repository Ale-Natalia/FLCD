/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

#ifndef YY_YY_GRAMMAR_TAB_H_INCLUDED
# define YY_YY_GRAMMAR_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    let = 258,
    const = 259,
    if = 260,
    then = 261,
    else = 262,
    while = 263,
    read = 264,
    len = 265,
    sin = 266,
    print = 267,
    BOOLEAN = 268,
    CHAR = 269,
    STRING = 270,
    INTEGER = 271,
    FLOAT = 272,
    id = 273,
    constant = 274,
    op_plus = 275,
    op_minus = 276,
    op_mul = 277,
    op_div = 278,
    op_eq = 279,
    op_gte = 280,
    op_lte = 281,
    op_gt = 282,
    op_lt = 283,
    op_or = 284,
    op_and = 285,
    op_mod = 286,
    op_eqeq = 287,
    op_dif = 288,
    op_pluseq = 289,
    op_minuseq = 290,
    op_muleq = 291,
    op_diveq = 292,
    op_modeq = 293,
    op_andeq = 294,
    op_oreq = 295,
    sep_open_par = 296,
    sep_closed_par = 297,
    sep_open_br = 298,
    sep_closed_br = 299,
    sep_open_curl = 300,
    sep_closed_curl = 301,
    sep_col = 302,
    sep_semicol = 303,
    sep_com = 304
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_GRAMMAR_TAB_H_INCLUDED  */
