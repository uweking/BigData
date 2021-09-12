When starting the .exe you will get a screen where you can choose your resoltion. the project was build for 1600:900, so it would be the best choice to stick with it.
When the programm is running you will see 3 parts. One for the visualization of the robot itself, one for displaying the data and the last one is for choosing your settings.

Data:
   Axis 1 -6:   	Shows the current local rotation value for the specific axis and in brackets the original value.
   TCP: 		Shows the current world position of the tool center point of the robot.
   dev. in mm:		Shows the deviation of the tcp compared to original value, this one only gets updated for each step.
   error <> X:		Shows how good a single value is compared to the original one. the given limits are highly subjectiv.


Settings:
   Data Set:		Choose your data set from where you later choose your cycle.
   Cycle to Simulate:	The specific Cycle you want to simulate. The mean deviation rises each 100 cycles.
   Mean Deviation:	Shows the mean deviation of the selected cycle
   Animation Speed:	Speed multiplier for the animation. 1 = 100%, 2 = 200%, 3 = 300%, ...
   Animation Time:	Also a speed multiplier. The normal Animation time for each step is 1 s. Be aware that animation speed is allready modifying this value.
   Error multiplier:	The multiplier is deactivated with the standard value 0. When activating it (1), a multiplier is added to the calculated rotation values
			of each axis. the multiplier is low when the rotation does not hava a big difference to the original value but will rise even more
			as the difference does.
   Run:			Starts the selected cycle with the given settings.
   Pause:		Pauses the running cycle after finishing the current step.
   Reset:		Resets the running/ paused cycle.


Data Sets:
   Sets 0 and 1 contain a number of simulated cycles which are grouped in batches of 100 cycles each. From one batch to another the mean deviation grows by 1%.
   Sets 2 and 3 contain the aggregated values of each batch.

   0:			100 batches -> 10k cycles
			starting mean deviation of 0.05%
   1:			50 batches -> 5k cycles
			starting mean deviation of 0.25%
   2:			1 cycle = 1 aggregated batch (mean values)
			100 cycles
			starting mean deviation of 0.05%
   3:			1 cycle = 1 aggregated batch (mean values)
			50 cycles
			starting mean deviation of 0.25%