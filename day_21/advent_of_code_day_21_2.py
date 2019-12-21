from common.intcodecomputer import CodeExecutor

def submit_script(springbot, script):
	for line in script:
		springbot.run(line)
		
	springbot.run('RUN')
	springbot.print_output_as_ascii()

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

springbot = CodeExecutor(program)
springbot.run([])

script = [
		   'NOT A T'
		   ,'AND D T'
		   ,'OR T J'
		   ,'NOT B T'
		   ,'AND D T'
		   ,'AND H T'
		   ,'OR T J'
		   ,'NOT C T'
		   ,'AND D T'
		   ,'AND H T'
		   ,'OR T J'
		 ]
submit_script(springbot, script)



