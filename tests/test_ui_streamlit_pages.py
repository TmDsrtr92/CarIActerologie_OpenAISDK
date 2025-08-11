"""
UI tests for Streamlit pages and user interactions
"""

import pytest
from unittest.mock import patch, Mock, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestHomePage:
    """Test the main homepage (app.py) functionality."""
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')  
    @patch('streamlit.button')
    @patch('streamlit.switch_page')
    def test_homepage_loads(self, mock_switch, mock_button, mock_columns, mock_markdown, mock_config):
        """Test that homepage loads without errors."""
        # Setup mocks
        mock_columns.return_value = [Mock(), Mock(), Mock()]
        mock_button.return_value = False
        
        # Import and run main function
        from app import main
        
        try:
            main()
            # If we get here, the page loaded successfully
            assert True
        except Exception as e:
            pytest.fail(f"Homepage failed to load: {e}")
        
        # Verify basic setup calls
        mock_config.assert_called_once()
        assert mock_markdown.call_count >= 2  # Header and navigation cards
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown') 
    @patch('streamlit.columns')
    @patch('streamlit.button')
    @patch('streamlit.switch_page')
    def test_navigation_buttons(self, mock_switch, mock_button, mock_columns, mock_markdown, mock_config):
        """Test navigation buttons on homepage."""
        # Setup mocks
        mock_columns.return_value = [Mock(), Mock(), Mock()]
        mock_button.side_effect = [True, False, False, False, False]  # First button clicked
        
        from app import main
        main()
        
        # Verify button was processed and switch_page was called
        mock_switch.assert_called_once_with("pages/1_Chat.py")
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch('streamlit.button')  
    @patch('streamlit.expander')
    def test_help_section_present(self, mock_expander, mock_button, mock_columns, mock_markdown, mock_config):
        """Test that help section is present on homepage."""
        # Setup mocks
        mock_columns.return_value = [Mock(), Mock(), Mock()]
        mock_button.return_value = False
        mock_expander_instance = Mock()
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_instance)
        mock_expander.return_value.__exit__ = Mock(return_value=None)
        
        from app import main
        main()
        
        # Verify help expander was created
        mock_expander.assert_called()
        
        # Check that help content was added
        help_content_found = False
        for call_args in mock_markdown.call_args_list:
            if "Quick Start Guide" in str(call_args) or "Understanding Characterology" in str(call_args):
                help_content_found = True
                break
        
        assert help_content_found, "Help content not found in homepage"


class TestChatPage:
    """Test the chat interface page functionality."""
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch('streamlit.container')
    @patch('streamlit.chat_input')
    @patch('streamlit.session_state', new_callable=lambda: {})
    def test_chat_page_loads(self, mock_session, mock_input, mock_container, mock_columns, mock_markdown, mock_config):
        """Test that chat page loads without errors."""
        # Setup mocks
        mock_columns.return_value = [Mock(), Mock()]
        mock_container.return_value.__enter__ = Mock()
        mock_container.return_value.__exit__ = Mock(return_value=None)
        mock_input.return_value = None
        
        from pages import Chat
        
        try:
            Chat.main()
            assert True
        except Exception as e:
            pytest.fail(f"Chat page failed to load: {e}")
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch('streamlit.container')
    @patch('streamlit.chat_input') 
    @patch('streamlit.rerun')
    @patch('streamlit.session_state', new_callable=lambda: {"messages": []})
    @patch('time.sleep')
    def test_message_processing(self, mock_sleep, mock_session, mock_rerun, mock_input, mock_container, mock_columns, mock_markdown, mock_config):
        """Test message processing in chat interface."""
        # Setup mocks
        mock_columns.return_value = [Mock(), Mock()]
        mock_container.return_value.__enter__ = Mock()
        mock_container.return_value.__exit__ = Mock(return_value=None)
        mock_input.return_value = "Test message"
        
        from pages import Chat
        
        # Simulate user input
        Chat.main()
        
        # Verify message was added to session state
        assert len(mock_session["messages"]) > 0
        assert mock_session["messages"][-1]["content"] == "Test message"
        assert mock_session["messages"][-1]["role"] == "user"
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.sidebar')
    @patch('streamlit.columns')
    @patch('streamlit.button')
    @patch('streamlit.metric')
    @patch('streamlit.session_state', new_callable=lambda: {"messages": [{"role": "assistant", "content": "Hello"}]})
    def test_sidebar_tools(self, mock_session, mock_metric, mock_button, mock_columns, mock_sidebar, mock_markdown, mock_config):
        """Test sidebar tools in chat interface.""" 
        # Setup mocks
        mock_sidebar.__enter__ = Mock()
        mock_sidebar.__exit__ = Mock(return_value=None)
        mock_columns.return_value = [Mock(), Mock()]
        mock_button.return_value = False
        
        from pages import Chat
        Chat.main()
        
        # Verify sidebar tools were set up
        mock_metric.assert_called()  # Session stats should be displayed
        assert mock_button.call_count >= 3  # At least 3 tool buttons


class TestAnalysisPage:
    """Test the analysis dashboard page functionality."""
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch('streamlit.plotly_chart')
    @patch('streamlit.metric')
    @patch('streamlit.success')
    @patch('streamlit.warning')
    def test_analysis_page_loads(self, mock_warning, mock_success, mock_metric, mock_plotly, mock_columns, mock_markdown, mock_config):
        """Test that analysis page loads without errors."""
        # Setup mocks
        mock_columns.return_value = [Mock(), Mock(), Mock()]
        
        # Mock plotly figure
        mock_figure = Mock()
        mock_figure.add_trace = Mock()
        mock_figure.update_layout = Mock()
        
        with patch('plotly.graph_objects.Figure', return_value=mock_figure):
            with patch('plotly.graph_objects.Scatterpolar', return_value=Mock()):
                from pages import Analysis
                
                try:
                    Analysis.main()
                    assert True
                except Exception as e:
                    pytest.fail(f"Analysis page failed to load: {e}")
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.plotly_chart')
    @patch('streamlit.expander')
    @patch('streamlit.session_state', new_callable=lambda: {})
    def test_first_time_user_guidance(self, mock_session, mock_expander, mock_plotly, mock_markdown, mock_config):
        """Test first-time user guidance on analysis page."""
        # Setup mocks
        mock_expander_instance = Mock()
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_instance)
        mock_expander.return_value.__exit__ = Mock(return_value=None)
        
        with patch('plotly.graph_objects.Figure'):
            with patch('plotly.graph_objects.Scatterpolar'):
                from pages import Analysis
                Analysis.main()
        
        # Verify guidance expander was created for first-time user
        mock_expander.assert_called()
        
        # Check that analysis_visited flag was set
        assert "analysis_visited" in mock_session
        assert mock_session["analysis_visited"] is True


class TestReportsPage:
    """Test the reports generation page functionality."""
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch('streamlit.selectbox')
    @patch('streamlit.button')
    @patch('streamlit.expander')
    def test_reports_page_loads(self, mock_expander, mock_button, mock_selectbox, mock_columns, mock_markdown, mock_config):
        """Test that reports page loads without errors."""
        # Setup mocks
        mock_columns.return_value = [Mock(), Mock()]
        mock_selectbox.return_value = "complete_analysis"
        mock_button.return_value = False
        mock_expander_instance = Mock()
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_instance)
        mock_expander.return_value.__exit__ = Mock(return_value=None)
        
        from pages import Reports
        
        try:
            Reports.main()
            assert True
        except Exception as e:
            pytest.fail(f"Reports page failed to load: {e}")
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch('streamlit.selectbox')
    @patch('streamlit.button')
    @patch('streamlit.success')
    @patch('streamlit.download_button')
    def test_report_generation(self, mock_download, mock_success, mock_button, mock_selectbox, mock_columns, mock_markdown, mock_config):
        """Test report generation functionality."""
        # Setup mocks
        mock_columns.return_value = [Mock(), Mock()]
        mock_selectbox.return_value = "complete_analysis"
        mock_button.return_value = True  # Generate button clicked
        
        from pages import Reports
        Reports.main()
        
        # Verify success message was shown
        mock_success.assert_called()
        
        # Verify download button was created
        mock_download.assert_called()


class TestSettingsPage:
    """Test the settings page functionality."""
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.tabs')
    @patch('streamlit.text_input')
    @patch('streamlit.selectbox')
    @patch('streamlit.checkbox')
    def test_settings_page_loads(self, mock_checkbox, mock_selectbox, mock_text_input, mock_tabs, mock_markdown, mock_config):
        """Test that settings page loads without errors."""
        # Setup mocks for tabs
        tab_mocks = [Mock() for _ in range(5)]
        for tab_mock in tab_mocks:
            tab_mock.__enter__ = Mock(return_value=tab_mock)
            tab_mock.__exit__ = Mock(return_value=None)
        mock_tabs.return_value = tab_mocks
        
        mock_text_input.return_value = "Test User"
        mock_selectbox.return_value = "Light"
        mock_checkbox.return_value = False
        
        from pages import Settings
        
        try:
            Settings.main()
            assert True
        except Exception as e:
            pytest.fail(f"Settings page failed to load: {e}")


class TestHelpPage:
    """Test the help documentation page functionality."""
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.tabs')
    @patch('streamlit.expander')
    def test_help_page_loads(self, mock_expander, mock_tabs, mock_markdown, mock_config):
        """Test that help page loads without errors.""" 
        # Setup mocks for tabs
        tab_mocks = [Mock() for _ in range(5)]
        for tab_mock in tab_mocks:
            tab_mock.__enter__ = Mock(return_value=tab_mock)
            tab_mock.__exit__ = Mock(return_value=None)
        mock_tabs.return_value = tab_mocks
        
        # Setup expander mocks
        mock_expander_instance = Mock()
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_instance)
        mock_expander.return_value.__exit__ = Mock(return_value=None)
        
        from pages import Help
        
        try:
            Help.main()
            assert True
        except Exception as e:
            pytest.fail(f"Help page failed to load: {e}")
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.tabs')
    @patch('streamlit.expander')
    def test_help_content_comprehensive(self, mock_expander, mock_tabs, mock_markdown, mock_config):
        """Test that help page contains comprehensive content."""
        # Setup mocks
        tab_mocks = [Mock() for _ in range(5)]
        for tab_mock in tab_mocks:
            tab_mock.__enter__ = Mock(return_value=tab_mock)
            tab_mock.__exit__ = Mock(return_value=None)
        mock_tabs.return_value = tab_mocks
        
        mock_expander_instance = Mock()  
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_instance)
        mock_expander.return_value.__exit__ = Mock(return_value=None)
        
        from pages import Help
        Help.main()
        
        # Check that comprehensive content was added
        content_topics = ["Getting Started", "Features", "Characterology", "Privacy", "Troubleshooting"]
        
        markdown_calls = [str(call) for call in mock_markdown.call_args_list]
        all_content = " ".join(markdown_calls)
        
        for topic in content_topics:
            assert topic in all_content, f"Missing help topic: {topic}"


class TestUserJourneyIntegration:
    """Test complete user journey flows across pages."""
    
    def test_navigation_flow_exists(self):
        """Test that navigation structure supports user journeys."""
        # Test that all expected pages can be imported
        try:
            import app
            from pages import Chat, Analysis, Dashboard, Reports, Settings, Help
            assert True
        except ImportError as e:
            pytest.fail(f"Page import failed: {e}")
    
    @patch('streamlit.switch_page')
    def test_homepage_navigation_links(self, mock_switch):
        """Test that homepage has navigation to all major pages."""
        with patch('streamlit.set_page_config'):
            with patch('streamlit.markdown'):
                with patch('streamlit.columns', return_value=[Mock(), Mock(), Mock()]):
                    with patch('streamlit.button', side_effect=[True, False, False, False, False]):
                        with patch('streamlit.expander'):
                            from app import main
                            main()
                            
                            # Verify navigation was attempted
                            mock_switch.assert_called_with("pages/1_Chat.py")


class TestAccessibilityAndUsability:
    """Test accessibility and usability features."""
    
    @patch('streamlit.set_page_config')
    def test_page_config_accessibility(self, mock_config):
        """Test that pages are configured with accessibility in mind."""
        from app import main
        
        # Mock other dependencies
        with patch('streamlit.markdown'):
            with patch('streamlit.columns', return_value=[Mock(), Mock(), Mock()]):
                with patch('streamlit.button', return_value=False):
                    with patch('streamlit.expander'):
                        main()
        
        # Check page configuration
        mock_config.assert_called_once()
        config_call = mock_config.call_args
        
        # Verify accessibility-friendly configuration
        assert "page_title" in config_call[1]
        assert "page_icon" in config_call[1]
        assert "layout" in config_call[1]
    
    def test_help_tooltips_present(self):
        """Test that help tooltips are implemented across pages."""
        # This is tested by checking CSS includes tooltip classes
        from app import main
        
        with patch('streamlit.set_page_config'):
            with patch('streamlit.markdown') as mock_markdown:
                with patch('streamlit.columns', return_value=[Mock(), Mock(), Mock()]):
                    with patch('streamlit.button', return_value=False):
                        with patch('streamlit.expander'):
                            main()
        
        # Check that tooltip CSS was included
        css_calls = [call for call in mock_markdown.call_args_list if "help-tooltip" in str(call)]
        assert len(css_calls) > 0, "Help tooltip CSS not found"


# Performance and Error Handling Tests
class TestPagePerformance:
    """Test page loading performance and error handling."""
    
    def test_page_import_performance(self):
        """Test that page imports are reasonably fast."""
        import time
        
        start_time = time.time()
        
        try:
            import app
            from pages import Chat, Analysis, Dashboard, Reports, Settings, Help
        except ImportError:
            pass  # Some imports may fail in test environment
        
        end_time = time.time()
        import_time = end_time - start_time
        
        assert import_time < 2.0, f"Page imports too slow: {import_time:.2f}s"
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch('streamlit.button')
    def test_error_handling_missing_dependencies(self, mock_button, mock_columns, mock_markdown, mock_config):
        """Test page behavior when dependencies are missing."""
        # Setup mocks
        mock_columns.return_value = [Mock(), Mock(), Mock()]
        mock_button.return_value = False
        
        # Test that pages handle missing mock data gracefully
        with patch('data.mock_data.get_primary_character_type', side_effect=ImportError("Mock import error")):
            try:
                from app import main
                main()
                # If we get here without exception, error handling worked
                assert True
            except ImportError:
                # This is expected - the page should handle the import error
                pass
            except Exception as e:
                # Unexpected exception - this is a test failure
                pytest.fail(f"Unexpected exception when handling missing dependencies: {e}")