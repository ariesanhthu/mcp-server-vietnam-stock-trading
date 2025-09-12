import pytest
import sys
from unittest.mock import patch, MagicMock
from vnstock_mcp.server import main


class TestCLI:
    """Test cases for command line interface functionality."""
    
    @patch('vnstock_mcp.server.server')
    def test_main_default_arguments(self, mock_server):
        """Test main function with default arguments (stdio)."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server']):
            main()
        
        mock_server.run.assert_called_once_with(transport='stdio', mount_path=None)
    
    @patch('vnstock_mcp.server.server')
    def test_main_stdio_transport(self, mock_server):
        """Test main function with explicit stdio transport."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'stdio']):
            main()
        
        mock_server.run.assert_called_once_with(transport='stdio', mount_path=None)
    
    @patch('vnstock_mcp.server.server')
    def test_main_sse_transport(self, mock_server):
        """Test main function with SSE transport."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'sse']):
            with patch('builtins.print') as mock_print:
                main()
        
        mock_server.run.assert_called_once_with(transport='sse', mount_path=None)
        # Check warning message was printed
        mock_print.assert_any_call(
            "Warning: Using SSE transport without mount-path. Default mount path will be used.",
            file=sys.stderr
        )
    
    @patch('vnstock_mcp.server.server')
    def test_main_sse_transport_with_mount_path(self, mock_server):
        """Test main function with SSE transport and mount path."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'sse', '--mount-path', '/vnstock']):
            main()
        
        mock_server.run.assert_called_once_with(transport='sse', mount_path='/vnstock')
    
    @patch('vnstock_mcp.server.server')
    def test_main_streamable_http_transport(self, mock_server):
        """Test main function with streamable-http transport."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'streamable-http']):
            main()
        
        mock_server.run.assert_called_once_with(transport='streamable-http', mount_path=None)
    
    @patch('vnstock_mcp.server.server')
    def test_main_mount_path_warning_with_stdio(self, mock_server):
        """Test warning when mount-path is used with stdio transport."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'stdio', '--mount-path', '/test']):
            with patch('builtins.print') as mock_print:
                main()
        
        mock_server.run.assert_called_once_with(transport='stdio', mount_path='/test')
        # Check warning message was printed
        mock_print.assert_any_call(
            "Warning: --mount-path is only used with SSE transport. Ignoring mount-path.",
            file=sys.stderr
        )
    
    @patch('vnstock_mcp.server.server')
    def test_main_mount_path_warning_with_streamable_http(self, mock_server):
        """Test warning when mount-path is used with streamable-http transport."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'streamable-http', '--mount-path', '/test']):
            with patch('builtins.print') as mock_print:
                main()
        
        mock_server.run.assert_called_once_with(transport='streamable-http', mount_path='/test')
        # Check warning message was printed
        mock_print.assert_any_call(
            "Warning: --mount-path is only used with SSE transport. Ignoring mount-path.",
            file=sys.stderr
        )
    
    def test_main_help_argument(self):
        """Test help argument exits with code 0."""
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
    
    def test_main_version_argument(self):
        """Test version argument exits with code 0."""
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--version']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
    
    def test_main_invalid_transport(self):
        """Test invalid transport argument exits with code 2."""
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'invalid']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 2
    
    @patch('vnstock_mcp.server.server')
    def test_main_keyboard_interrupt(self, mock_server):
        """Test KeyboardInterrupt handling."""
        mock_server.run = MagicMock(side_effect=KeyboardInterrupt())
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    main()
        
        assert exc_info.value.code == 0
        mock_print.assert_any_call("\nServer stopped by user.", file=sys.stderr)
    
    @patch('vnstock_mcp.server.server')
    def test_main_general_exception(self, mock_server):
        """Test general exception handling."""
        mock_server.run = MagicMock(side_effect=Exception("Test error"))
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    main()
        
        assert exc_info.value.code == 1
        mock_print.assert_any_call("Error starting server: Test error", file=sys.stderr)
    
    @patch('vnstock_mcp.server.server')
    def test_main_short_arguments(self, mock_server):
        """Test short argument forms."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '-t', 'sse', '-m', '/vnstock']):
            main()
        
        mock_server.run.assert_called_once_with(transport='sse', mount_path='/vnstock')
    
    @patch('vnstock_mcp.server.server')  
    def test_main_prints_startup_messages(self, mock_server):
        """Test that startup messages are printed to stderr."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'sse', '--mount-path', '/vnstock']):
            with patch('builtins.print') as mock_print:
                main()
        
        # Check startup messages
        mock_print.assert_any_call(
            "Starting VNStock MCP Server with sse transport...",
            file=sys.stderr
        )
        mock_print.assert_any_call(
            "SSE mount path: /vnstock",
            file=sys.stderr
        )
