workflow HelloWorld {

	String hello_world_string
  	String hello_world_string2

  
  	call echo { 
  		input: s = hello_world_string, 
               s2= hello_world_string2
	}
}

task echo {

	String s
    String s2

	command {
    	echo ${s}!
        echo And ${s2}!
    }
    runtime {
    	docker: "ubuntu"
        cpu: 1
        disks: "local-disk 1 HDD"
        noAddress: true
    }
    output {
    	String out = read_string(stdout())
    }
}