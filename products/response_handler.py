from rest_framework.response import Response
from rest_framework import status


class StandardResponse:
    """
    Standardized API response handler for consistent frontend integration
    """
    
    @staticmethod
    def success(data=None, message="Operation successful", status_code=status.HTTP_200_OK):
        """
        Standard success response format
        """
        response_data = {
            "success": True,
            "status_code": status_code,
            "message": message,
            "data": data,
            "errors": None
        }
        return Response(response_data, status=status_code)
    
    @staticmethod
    def created(data=None, message="Resource created successfully"):
        """
        Standard creation success response
        """
        response_data = {
            "success": True,
            "status_code": status.HTTP_201_CREATED,
            "message": message,
            "data": data,
            "errors": None
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    @staticmethod
    def not_found(message="Resource not found"):
        """
        Standard 404 not found response
        """
        response_data = {
            "success": False,
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": message,
            "data": None,
            "errors": None
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def validation_error(errors, message="Validation failed"):
        """
        Standard validation error response
        """
        response_data = {
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": message,
            "data": None,
            "errors": errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def empty_list(message="No data found"):
        """
        Standard empty list response
        """
        response_data = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": message,
            "data": [],
            "errors": None
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    @staticmethod
    def server_error(message="Internal server error"):
        """
        Standard server error response
        """
        response_data = {
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": message,
            "data": None,
            "errors": None
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)