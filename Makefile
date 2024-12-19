all: scanner
	g++ -std=c++11 -o scanner scanner.cpp -Wall
scanner: scanner.cpp
	g++ -std=c++11 -o scanner scanner.cpp -Wall
tokens: scanner
	./scanner example_inputs/simple1.hl -o tokenized_inputs/simple1.txt
	./scanner example_inputs/simple2.hl -o tokenized_inputs/simple2.txt
	./scanner example_inputs/simple3.hl -o tokenized_inputs/simple3.txt
	./scanner example_inputs/simple4.hl -o tokenized_inputs/simple4.txt
	./scanner example_inputs/simple5.hl -o tokenized_inputs/simple5.txt


ast: tokens
	python3 tph_parser.py tokenized_inputs/simple1.txt
	python3 tph_parser.py tokenized_inputs/simple2.txt
	python3 tph_parser.py tokenized_inputs/simple3.txt
	python3 tph_parser.py tokenized_inputs/simple4.txt
	python3 tph_parser.py tokenized_inputs/simple5.txt

ast-1: tokens
	python3 tph_parser.py tokenized_inputs/simple1.txt
ast-2: tokens
	python3 tph_parser.py tokenized_inputs/simple2.txt
ast-3: tokens
	python3 tph_parser.py tokenized_inputs/simple3.txt
ast-4: tokens
	python3 tph_parser.py tokenized_inputs/simple4.txt
ast-5: tokens
	python3 tph_parser.py tokenized_inputs/simple5.txt

ast-files: tokens
	python3 tph_parser.py tokenized_inputs/simple1.txt -o ast_outputs/output1.txt
	python3 tph_parser.py tokenized_inputs/simple2.txt -o ast_outputs/output2.txt
	python3 tph_parser.py tokenized_inputs/simple3.txt -o ast_outputs/output3.txt
	python3 tph_parser.py tokenized_inputs/simple4.txt -o ast_outputs/output4.txt
	python3 tph_parser.py tokenized_inputs/simple5.txt -o ast_outputs/output5.txt

ast-file-1: tokens
	python3 tph_parser.py tokenized_inputs/simple1.txt -o ast_outputs/output1.txt
ast-file-2: tokens
	python3 tph_parser.py tokenized_inputs/simple2.txt -o ast_outputs/output2.txt
ast-file-3:	tokens
	python3 tph_parser.py tokenized_inputs/simple3.txt -o ast_outputs/output3.txt
ast-file-4: tokens
	python3 tph_parser.py tokenized_inputs/simple4.txt -o ast_outputs/output4.txt
ast-file-5: tokens
	python3 tph_parser.py tokenized_inputs/simple5.txt -o ast_outputs/output5.txt

build-directory:
	mkdir -p tokenized_inputs
	mkdir -p ast_outputs
	mkdir -p generated_code/test1
	mkdir -p generated_code/test2
	mkdir -p generated_code/test3
	mkdir -p generated_code/test4
	mkdir -p generated_code/test5
	mkdir -p code_template

code-gen:
	python3 code_generator_parsing_input.py ast_outputs/output1.txt -o generated_code/test1/generator.py
	python3 code_generator_parsing_input.py ast_outputs/output2.txt -o generated_code/test2/generator.py
	python3 code_generator_parsing_input.py ast_outputs/output3.txt -o generated_code/test3/generator.py
	python3 code_generator_parsing_input.py ast_outputs/output4.txt -o generated_code/test4/generator.py
	python3 code_generator_parsing_input.py ast_outputs/output5.txt -o generated_code/test5/generator.py

code-gen-1-dbg:
	python3 code_generator_parsing_input.py ast_outputs/output1.txt

code-gen-2-dbg:
	python3 code_generator_parsing_input.py ast_outputs/output2.txt

code-gen-3-dbg:
	python3 code_generator_parsing_input.py ast_outputs/output3.txt

code-gen-4-dbg:
	python3 code_generator_parsing_input.py ast_outputs/output4.txt

code-gen-5-dbg:
	python3 code_generator_parsing_input.py ast_outputs/output5.txt

code-gen-1:
	python3 code_generator_parsing_input.py ast_outputs/output1.txt -o generated_code/test1/generator.py

code-gen-2:
	python3 code_generator_parsing_input.py ast_outputs/output2.txt -o generated_code/test2/generator.py

code-gen-3:
	python3 code_generator_parsing_input.py ast_outputs/output3.txt -o generated_code/test3/generator.py

code-gen-4:
	python3 code_generator_parsing_input.py ast_outputs/output4.txt -o generated_code/test4/generator.py

code-gen-5:
	python3 code_generator_parsing_input.py ast_outputs/output5.txt -o generated_code/test5/generator.py

code-exec:
	cd generated_code/test1 && python3 generator.py && cd ../..
	cd generated_code/test2 && python3 generator.py && cd ../..
	cd generated_code/test3 && python3 generator.py && cd ../..
	cd generated_code/test4 && python3 generator.py && cd ../..
	cd generated_code/test5 && python3 generator.py && cd ../..

install:
	cp generated_code/test1/FC_0/huangemmplt.hpp huangemmplt_stratus/hw/src/.
	cp generated_code/test1/FC_0/init_data.hpp huangemmplt_stratus/hw/tb/.
	cp generated_code/test1/FC_0/memlist.txt huangemmplt_stratus/hw/.

install-2:
	cp generated_code/test2/FC_0/huangemmplt.hpp huangemmplt_stratus/hw/src/.
	cp generated_code/test2/FC_0/init_data.hpp huangemmplt_stratus/hw/tb/.
	cp generated_code/test2/FC_0/memlist.txt huangemmplt_stratus/hw/.

install-3:
	cp generated_code/test3/FC_0/huangemmplt.hpp huangemmplt_stratus/hw/src/.
	cp generated_code/test3/FC_0/init_data.hpp huangemmplt_stratus/hw/tb/.
	cp generated_code/test3/FC_0/memlist.txt huangemmplt_stratus/hw/.

install-4:
	cp generated_code/test4/FC_0/huangemmplt.hpp huangemmplt_stratus/hw/src/.
	cp generated_code/test4/FC_0/init_data.hpp huangemmplt_stratus/hw/tb/.
	cp generated_code/test4/FC_0/memlist.txt huangemmplt_stratus/hw/.

install-5:
	cp generated_code/test5/FC_0/huangemmplt.hpp huangemmplt_stratus/hw/src/.
	cp generated_code/test5/FC_0/init_data.hpp huangemmplt_stratus/hw/tb/.
	cp generated_code/test5/FC_0/memlist.txt huangemmplt_stratus/hw/.

demo-opt:
	python3 code_generator_parsing_input.py ast_outputs/output4.txt -o generated_code/test4/not_optimized_generator.py

demo-opt-print:
	echo "=========================="
	python3 code_generator_parsing_input.py ast_outputs/output4.txt


code-gen-clean:
	rm -rf generated_code/*
	mkdir -p generated_code/test1
	mkdir -p generated_code/test2
	mkdir -p generated_code/test3
	mkdir -p generated_code/test4
	mkdir -p generated_code/test5

clean:
	rm -f scanner
	rm -rf tokenized_inputs/*
	rm -rf ast_outputs/*
	rm -rf generated_code/*
	mkdir -p tokenized_inputs
	mkdir -p ast_outputs
	mkdir -p generated_code/test1
	mkdir -p generated_code/test2
	mkdir -p generated_code/test3
	mkdir -p generated_code/test4
	mkdir -p generated_code/test5