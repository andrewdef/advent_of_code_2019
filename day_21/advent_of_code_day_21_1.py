from common.intcodecomputer import CodeExecutor

def submit_script(springbot, script):
	for line in script:
		springbot.run(line)
		
	springbot.run('WALK')
	springbot.print_output_as_ascii()

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

springbot = CodeExecutor(program)
springbot.run([])

script = [
			'NOT B T'
		   ,'NOT C J'
		   ,'AND D T'
		   ,'AND T J'
		   ,'NOT A T'
		   ,'AND D T'
		   ,'OR T J'
		   ,'NOT C T'
		   ,'AND D T'
		   ,'OR T J'		   
		 ]
submit_script(springbot, script)



