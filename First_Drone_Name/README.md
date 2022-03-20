# First drone name
First of all we need a name for this drone.

## Requirements
The drone will weight less than 250 grams and have a maximum speed of 19 m/s.

The drone to flight will require the following components:
- Frame
- Flight controller
- A GPS
- Motors
- Propellers
- ESCs
- Comms
- Battery
- Power module

## Design
To simplify the design and reduce weight the required components are merged in 4
subsystems:
- The [PCB](./Board/README.md) that will accomodate all eletronics. The GPS, the Flight controller, the ESCs, the Comms and the Power module are accounted for in this folder.
- A [supporting frame](./Frame/README.md) to sustain produced stress. The Frame is accounted for in this folder.
- [Motors and propellers](./Propulsion/README.md). Motor and Propellers are accounted for in this folder.
- A [battery](./Battery/README.md). The Battery is accounted for in this folder.
