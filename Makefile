# Makefile for source rpm: cpio
# $Id$
NAME := cpio
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
