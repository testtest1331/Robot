from commands2 import Subsystem
from phoenix6 import hardware, controls, configs, signals

class ShooterSubsystem(Subsystem):
    def __init__(self):
        super().__init__()

        # 1. Define your motors (Change IDs if needed)
        self.flywheel = hardware.TalonFX(49)  # Your Kraken X60
        self.feeder = hardware.TalonFX(48)    # Your Intake/Feeder Motor

        # 2. Configure the Kraken (Current Limits are CRITICAL)
        kraken_config = configs.TalonFXConfiguration()
        
        # Supply Limit: Protects the breaker/battery (40 Amps)
        kraken_config.current_limits.supply_current_limit = 40.0
        kraken_config.current_limits.supply_current_limit_enable = True
        
        # Stator Limit: Protects the motor from heat (80 Amps)
        kraken_config.current_limits.stator_current_limit = 80.0
        kraken_config.current_limits.stator_current_limit_enable = True

        # Apply configs
        self.flywheel.configurator.apply(kraken_config)

    def run_flywheel(self, velocity_rps: float):
        """
        Spins the main shooter wheel.
        Using VelocityVoltage for consistent speed.
        """
        # Note: You need to tune PID for this to work perfectly!
        # For now, we use VoltageOut for testing if you haven't tuned yet.
        # self.flywheel.set_control(controls.VelocityVoltage(velocity_rps))
        
        # Simpler version for today: Voltage (0-12V)
        self.flywheel.set_control(controls.VoltageOut(velocity_rps)) 

    def run_feeder(self, percent: float):
        """
        Runs the intake/feeder motor.
        Range: -1.0 to 1.0
        """
        self.feeder.set_control(controls.DutyCycleOut(percent))

    def stop(self):
        """Turn everything off safely."""
        self.flywheel.set_control(controls.NeutralOut())
        self.feeder.set_control(controls.NeutralOut())