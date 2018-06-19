## Process this file with automake to produce Makefile.in
AM_CFLAGS = -g -Og -Wall -Wextra -Werror

# Library
pkgconfig_DATA = sfork.pc
lib_LTLIBRARIES = libsfork.la

libsfork_la_SOURCES = src/sfork.c src/sfork_x86_64.S
include_HEADERS = src/sfork.h

# Tests
check_PROGRAMS = test_sfork
test_sfork_SOURCES = src/test_sfork_main.c
test_sfork_LDADD = libsfork.la
