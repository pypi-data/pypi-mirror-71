import logging

_LOGGER = logging.getLogger(__name__)

class LoxJalousie:
    """Class for node abstraction."""

    def __init__(self, id, name, cat, device_type):
        self._id = id
        self._name = name
        self._cat = cat
        self._device_type = device_type
        self._position = False
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
    def position(self):
        return self._position

    def register_async_callback(self, async_callback):
        #_LOGGER.debug("register_async_callback")
        self.async_callbacks.append(async_callback)

    def unregister_async_callback(self, callback):
        #_LOGGER.debug("unregister_async_callback")
        if callback in self.async_callbacks:
            self.async_callbacks.remove(callback)

    #def async_set_position(self, position):
    #    _LOGGER.debug("{0} [{1}] async_set_position() position={2}".format(self._id, self._name, position))

    #def async_stop(self):
    #    _LOGGER.debug("{0} [{1}] async_stop()".format(self._id, self._name))

    def async_update(self):
        for async_signal_update in self.async_callbacks:
            _LOGGER.debug("{0} [{1}] async_update() state={2}".format(self._id, self._name, self._position))
            async_signal_update()

    def set_value(self, stateName, value):
        if self._device_type == "Jalousie" and stateName == "position":
            _LOGGER.debug("{0} [{1}] Set Jalousie - state={2}".format(self._id, self._name, value))

            self._position = value

            self.async_update()

        else:
            _LOGGER.debug("{0} [{1}] NotSet {2} - {3}={4}".format(self._id, self._name, self._device_type, stateName, value))
