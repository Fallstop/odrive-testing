from odrv_wrapper import Odrive_Arm

print("Initialize")
arm = Odrive_Arm()
x_location = float(input("Move X to:"))
arm.move_axis("X",x_location)
print("Done")