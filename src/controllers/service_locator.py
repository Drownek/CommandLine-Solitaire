from typing import Dict, Any, Type, TypeVar

T = TypeVar('T')

class ServiceLocator:
    """
    A service locator implementation that provides a central registry for controllers and services.
    
    This class allows components to access controllers and services without having to pass them
    through the entire widget hierarchy. It follows the service locator pattern, which is a design
    pattern that provides a centralized registry of services.
    
    Usage:
        # Register a service
        ServiceLocator.register(CardInteractController, card_controller_instance)
        
        # Get a service
        controller = ServiceLocator.get(CardInteractController)
    """
    
    _services: Dict[Type, Any] = {}
    
    @classmethod
    def register(cls, service_type: Type[T], instance: T) -> None:
        """
        Register a service instance with the service locator.
        
        Args:
            service_type: The type (class) of the service
            instance: The instance of the service to register
        """
        cls._services[service_type] = instance
    
    @classmethod
    def get(cls, service_type: Type[T]) -> T:
        """
        Get a service instance from the service locator.
        
        Args:
            service_type: The type (class) of the service to retrieve
            
        Returns:
            The instance of the requested service
            
        Raises:
            KeyError: If the requested service is not registered
        """
        if service_type not in cls._services:
            raise KeyError(f"Service of type {service_type.__name__} not registered")
        return cls._services[service_type]