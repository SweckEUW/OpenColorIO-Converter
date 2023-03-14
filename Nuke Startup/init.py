import nuke

print("Nuke Shotgrid init.py | Setting Color Managmenet")

nuke.knobDefault("Root.colorManagement", "OCIO")
nuke.knobDefault('Root.OCIO_config', 'custom')
nuke.knobDefault('Root.customOCIOConfigPath', "R:/00_pipeline/OCIO Configs/aces_1.0.1/RATZ_OCIO_config_v001.ocio")