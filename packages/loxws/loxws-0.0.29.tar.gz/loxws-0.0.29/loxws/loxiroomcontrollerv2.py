import logging

_LOGGER = logging.getLogger(__name__)

class LoxIntelligentRoomControllerV2:
    """Class for node abstraction."""

    def __init__(self, id, name, device_type):
        self._id = id
        self._name = name
        self._device_type = device_type
        self._current_temp = 0
        self._target_temp = 0
        self._hvac_mode = 0
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
    def current_temp(self):
        return self._current_temp

    @property
    def target_temp(self):
        return self._target_temp

    @property
    def hvac_mode(self):
        return self._hvac_mode

    def register_async_callback(self, async_callback):
        #_LOGGER.debug("register_async_callback")
        self.async_callbacks.append(async_callback)

    def unregister_async_callback(self, callback):
        #_LOGGER.debug("unregister_async_callback")
        if callback in self.async_callbacks:
            self.async_callbacks.remove(callback)

    def async_update(self):
        for async_signal_update in self.async_callbacks:
            _LOGGER.debug("{0} [{1}] async_update() ".format(self._id, self._name))
            async_signal_update()

    def set_value(self, stateName, value):
        if self._device_type == "IRoomControllerV2" and stateName == "tempActual":
            _LOGGER.debug("{0} [{1}] Current Temp - state={2}".format(self._id, self._name, value))
            self._current_temp = value

            self.async_update()

        if self._device_type == "IRoomControllerV2" and stateName == "tempTarget":
            _LOGGER.debug("{0} [{1}] Target Temp - state={2}".format(self._id, self._name, value))
            self._target_temp = value

            self.async_update()

        if self._device_type == "IRoomControllerV2" and stateName == "demand":
            _LOGGER.debug("{0} [{1}] Demand - state={2}".format(self._id, self._name, value))
            self._hvac_mode = value

            self.async_update()

        else:
            _LOGGER.debug("{0} [{1}] NotSet {2} - {3}={4}".format(self._id, self._name, self._device_type, stateName, value))
