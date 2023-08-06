import logging

_LOGGER = logging.getLogger(__name__)

class LoxInfoOnlyAnalog:
    """Class for node abstraction."""

    def __init__(self, id, name, device_type, structure):
        self._id = id
        self._name = name
        self._device_type = device_type
        self._structure = structure
        self._state = False
        self.async_callbacks = []
            
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def device_type(self):
        return self._device_type

    @property
    def manufacturername(self):
        return 'Loxone'    

    @property
    def state(self):
        return self._state

    @property
    def format(self):
        control_format = ""
        if 'details' in self._structure:
            if 'format' in self._structure["details"]:
                control_format = self._structure["details"]["format"]
                _LOGGER.debug("format: {0}".format(control_format))
        return control_format

    def register_async_callback(self, async_callback):
        #_LOGGER.debug("register_async_callback")
        self.async_callbacks.append(async_callback)

    def unregister_async_callback(self, callback):
        #_LOGGER.debug("unregister_async_callback")
        if callback in self.async_callbacks:
            self.async_callbacks.remove(callback)

    def async_update(self):
        for async_signal_update in self.async_callbacks:
            _LOGGER.debug("{0} [{1}] async_update() state={2}".format(self._id, self._name, self._state))
            async_signal_update()

    def set_value(self, stateName, value):
        if self._device_type == "InfoOnlyAnalog" and stateName == "value":
            _LOGGER.debug("{0} [{1}] Set Sensor - state={2}".format(self._id, self._name, value))
            self._state = value

            self.async_update()

        else:
            _LOGGER.debug("{0} [{1}] NotSet {2} - {3}={4}".format(self._id, self._name, self._device_type, stateName, value))
