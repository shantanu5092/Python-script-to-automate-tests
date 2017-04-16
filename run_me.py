#!/usr/bin/python
import os

def create_top(design):
  top_file = open("../Backup/top.sv","w")
  top_file.write("""
  //************************
  //   Top File
  //************************
  """.format(""))
  
  line = "`include \"../Backup/" + design + "\""
  top_file.write(line) 
  top_file.write("""

 
  //************************
  //   Top File
  //************************
//  `include "fifo.sv"

    //
// A debug driver to check code syntax
//


//`include "fifo5.sv"
`include "fifoif.sv"
//`include "global.sv"
//`define parameter busw=32,enteries=15;
//`define parameter enteries=15;
import uvm_pkg::*;
//import uart_pkg::*;
//`include "global.sv"
`include "fifo_uvm.sv"

module top();


logic [31:0] busw=275,enteries = 167;



fifoif q();
fifo #(32,32) f(q.fif);

reg [31:0] exp[$];

initial begin
  q.clk=1;
  repeat(1000000) begin
    #5 q.clk=~q.clk;
  end
end


initial
  begin
    
    uvm_config_db#(virtual fifoif )::set(null, "uvm_test_top", "fifoif" ,q );
    run_test("fifo_test");
 
  end
initial begin
  $dumpfile("fifo.vpd");
  $dumpvars();
end




endmodule : top
  
 """.format(""))
  
  top_file.close()

#h_w = [(15,32),(7,9),(7,167),(188,32),(188,167),(275,9),(275,32),(275,167)]   #added for basic
top_res = open("final_result_275_167.txt","w")
for i in range(0,11,1):   #changing to 1 (0,11,1) 11->1
    if (i==0):
      file = "fifo.sv"
    else:
      file = "fifo" + str(i) + ".sv"
    create_top(file)
    res_file = "test_fifo_275_167_" + str(i) + "_result.txt"
    """cmd = "vcs -ntb_opts uvm-1.1 -timescale= -sverilog -debug_all +UVM_MAX_QUIT_COUNT=10 +define+busw=" + str(j[1]) + " +define+enteries=" + str(j[0]) + "+lint=PCWM +vcsd +UVM_TESTNAME=fifo_sample_test +incdir+../sv +incdir+../tb -R -l simv.log .. ../279HW4/fifoif.sv ../279HW4/top.sv -cm line+cond+fsm+branch -cm_dir coverage +UVM_TIMEOUT=5000000000 | tee " + res_file"""
    cmd = "../Backup/sv_uvm top.sv | tee " + res_file
    os.system(cmd)
    res = open(res_file,"r")
    flag = "Fail"
    for line in res:
      if ("UVM_ERROR :    0" in line):
        flag = "Pa"
      if ("UVM_FATAL :    0" in line):
        flag = flag + ("ss")
    if (flag == "Pass"):
      flag = " Pass\n"
    else:
      flag = " Fail \n"
    
    res = open(res_file,"r")
    if flag == " Fail \n":
      for line in res:
        if "UVM_ERROR" in line:
          err_line = line
          l = res_file  + " --> " + flag[:-1] + " --> " + err_line + "\n"
          break
    else:      
      l = res_file  + " --> " + flag 
    
    top_res.write(l) 
    #top_res.write(res_file)
top_res.close()
