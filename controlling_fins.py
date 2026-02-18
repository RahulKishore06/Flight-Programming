def add_afs_canards(
        self,
        drag_coefficient_curve,
        controller_function,
        sampling_rate,
        clamp=True,
        reference_area=None,
        initial_observed_variables=None,
        override_rocket_drag=False,
        return_controller=False,
        name="AirBrakes",
        controller_name="AirBrakes Controller",
    ):
        """Creates a new air brakes system, storing its parameters such as
        drag coefficient curve, controller function, sampling rate, and
        reference area.

        Parameters
        ----------
        drag_coefficient_curve : int, float, callable, array, string, Function
            This parameter represents the drag coefficient associated with the
            air brakes and/or the entire rocket, depending on the value of
            ``override_rocket_drag``.

            - If a constant, it should be an integer or a float representing a
              fixed drag coefficient value.
            - If a function, it must take two parameters: deployment level and
              Mach number, and return the drag coefficient. This function allows
              for dynamic computation based on deployment and Mach number.
            - If an array, it should be a 2D array with three columns: the first
              column for deployment level, the second for Mach number, and the
              third for the corresponding drag coefficient.
            - If a string, it should be the path to a .csv or .txt file. The
              file must contain three columns: the first for deployment level,
              the second for Mach number, and the third for the drag
              coefficient.
            - If a Function, it must take two parameters: deployment level and
              Mach number, and return the drag coefficient.

            .. note:: For ``override_rocket_drag = False``, at
                deployment level 0, the drag coefficient is assumed to be 0,
                independent of the input drag coefficient curve. This means that
                the simulation always considers that at a deployment level of 0,
                the air brakes are completely retracted and do not contribute to
                the drag of the rocket.

        controller_function : function, callable
            An user-defined function responsible for controlling the simulation.
            This function is expected to take the following arguments, in order:

            1. `time` (float): The current simulation time in seconds.
            2. `sampling_rate` (float): The rate at which the controller
               function is called, measured in Hertz (Hz).
            3. `state` (list): The state vector of the simulation, structured as
               `[x, y, z, vx, vy, vz, e0, e1, e2, e3, wx, wy, wz]`.
            4. `state_history` (list): A record of the rocket's state at each
               step throughout the simulation. The state_history is organized as a
               list of lists, with each sublist containing a state vector. The last
               item in the list always corresponds to the previous state vector,
               providing a chronological sequence of the rocket's evolving states.
            5. `observed_variables` (list): A list containing the variables that
               the controller function returns. The initial value in the first
               step of the simulation of this list is provided by the
               `initial_observed_variables` argument.
            6. `interactive_objects` (list): A list containing the objects that
               the controller function can interact with. The objects are
               listed in the same order as they are provided in the
               `interactive_objects`
            7. `sensors` (list): A list of sensors that are attached to the
                rocket. The most recent measurements of the sensors are provided
                with the ``sensor.measurement`` attribute. The sensors are
                listed in the same order as they are added to the rocket
               ``interactive_objects``

            This function will be called during the simulation at the specified
            sampling rate. The function should evaluate and change the observed
            objects as needed. The function should return None.

            .. note::

                The function will be called according to the sampling rate specified.

        sampling_rate : float
            The sampling rate of the controller function in Hertz (Hz). This
            means that the controller function will be called every
            `1/sampling_rate` seconds.
        clamp : bool, optional
            If True, the simulation will clamp the deployment level to 0 or 1 if
            the deployment level is out of bounds. If False, the simulation will
            not clamp the deployment level and will instead raise a warning if
            the deployment level is out of bounds. Default is True.
        reference_area : float, optional
            Reference area used to calculate the drag force of the air brakes
            from the drag coefficient curve. If None, which is default, use
            rocket section area. Must be given in squared meters.
        initial_observed_variables : list, optional
            A list of the initial values of the variables that the controller
            function returns. This list is used to initialize the
            `observed_variables` argument of the controller function. The
            default value is None, which initializes the list as an empty list.
        override_rocket_drag : bool, optional
            If False, the air brakes drag coefficient will be added to the
            rocket's power off drag coefficient curve. If True, during the
            simulation, the rocket's power off drag will be ignored and the air
            brakes drag coefficient will be used for the entire rocket instead.
            Default is False.
        return_controller : bool, optional
            If True, the function will return the controller object created.
            Default is False.
        name : string, optional
            AirBrakes name, such as drogue and main. Has no impact in
            simulation, as it is only used to display data in a more
            organized matter.
        controller_name : string, optional
            Controller name. Has no impact in simulation, as it is only used to
            display data in a more organized matter.

        Returns
        -------
        air_brakes : AirBrakes
            AirBrakes object created.
        controller : Controller
            Controller object created.
        """
        reference_area = reference_area if reference_area is not None else self.area
        air_brakes = AirBrakes(
            drag_coefficient_curve=drag_coefficient_curve,
            reference_area=reference_area,
            clamp=clamp,
            override_rocket_drag=override_rocket_drag,
            deployment_level=0,
            name=name,
        )
        _controller = _Controller(
            interactive_objects=air_brakes,
            controller_function=controller_function,
            sampling_rate=sampling_rate,
            initial_observed_variables=initial_observed_variables,
            name=controller_name,
        )
        self.air_brakes.append(air_brakes)
        self._add_controllers(_controller)
        if return_controller:
            return air_brakes, _controller
        else:
            return air_brakes