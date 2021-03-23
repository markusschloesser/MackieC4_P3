from types import ModuleType


class Application(ModuleType):
    pass

    @staticmethod
    def combine_apcs():
        """
        Returns true if multiple APCs should be combined. C++ signature :  bool combine_apcs()
        """
        pass

    @staticmethod
    def encrypt_challenge(dongle1, dongle2, key_index=0):
        """
        Returns an encrypted challenge based on the TEA algortithm C++ signature :  boost::python::tuple encrypt_challenge(int,int [,int=0])
        :param dongle1: dongle1
        :type dongle1: int
        :param dongle2: dongle2
        :type dongle2: int
        :param key_index: key_index defaults to 0 
        :type key_index: int
        :rtype: tuple
        """
        pass

    @staticmethod
    def encrypt_challenge2(arg1):
        """
        Returns the UMAC hash for the given challenge. C++ signature :  int encrypt_challenge2(int)
        :param arg1: arg1
        :type arg1: int
        :rtype: int
        """
        pass

    @staticmethod
    def get_application():
        """
        Returns the application instance. C++ signature :  TWeakPtr<TPyHandle<ASongApp> > get_application()
        """
        pass

    @staticmethod
    def get_random_int(arg1, arg2):
        """
        Returns a random integer from the given range. C++ signature :  int get_random_int(int,int)
        :param arg1: arg1
        :type arg1: int
        :param arg2: arg2
        :type arg2: int
        :rtype: int
        """
        pass

    class Application(object):
        def __init__(self, *a, *k):
            """
            This class represents the Live application.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def browser(self):
            """
            Returns an interface to the browser.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Returns the canonical parent of the application.
            """
            pass

        @property
        def control_surfaces(self):
            """
            Const access to a list of the control surfaces selected in preferences, in the same order.The list contains None if no control surface is active at that index.
            """
            pass

        @property
        def current_dialog_button_count(self):
            """
            Number of buttons on the current dialog.
            """
            pass

        @property
        def current_dialog_message(self):
            """
            Text of the last dialog that appeared; Empty if all dialogs just disappeared.
            """
            pass

        @property
        def open_dialog_count(self):
            """
            The number of open dialogs in Live. 0 if not dialog is open.
            """
            pass

        @property
        def unavailable_features(self):
            """
            List of features that are unavailable due to limitations of the current Live edition.
            """
            pass

        @property
        def view(self):
            """
            Returns the applications view component.
            """
            pass

        def add_control_surfaces_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "control_surfaces" has changed. C++ signature :  void add_control_surfaces_listener(TPyHandle<ASongApp>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_open_dialog_count_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "open_dialog_count" has changed. C++ signature :  void add_open_dialog_count_listener(TPyHandle<ASongApp>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_unavailable_features_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "unavailable_features" has changed. C++ signature :  void add_unavailable_features_listener(TPyHandle<ASongApp>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def control_surfaces_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "control_surfaces". C++ signature :  bool control_surfaces_has_listener(TPyHandle<ASongApp>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def get_bugfix_version(self, arg1):
            """
            Returns an integer representing the bugfix version of Live. C++ signature :  int get_bugfix_version(TPyHandle<ASongApp>)
            :param arg1: arg1
            :type arg1: Application
            :rtype: int
            """
            pass

        def get_document(self, arg1):
            """
            Returns the current Live Set. C++ signature :  TWeakPtr<TPyHandle<ASong> > get_document(TPyHandle<ASongApp>)
            :param arg1: arg1
            :type arg1: Application
            :rtype: Song
            """
            pass

        def get_major_version(self, arg1):
            """
            Returns an integer representing the major version of Live. C++ signature :  int get_major_version(TPyHandle<ASongApp>)
            :param arg1: arg1
            :type arg1: Application
            :rtype: int
            """
            pass

        def get_minor_version(self, arg1):
            """
            Returns an integer representing the minor version of Live. C++ signature :  int get_minor_version(TPyHandle<ASongApp>)
            :param arg1: arg1
            :type arg1: Application
            :rtype: int
            """
            pass

        def has_option(self, arg1, arg2):
            """
            Returns True if the given entry exists in Options.txt, False otherwise. C++ signature :  bool has_option(TPyHandle<ASongApp>,TString)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def open_dialog_count_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "open_dialog_count". C++ signature :  bool open_dialog_count_has_listener(TPyHandle<ASongApp>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def press_current_dialog_button(self, arg1, arg2):
            """
            Press a button, by index, on the current message box. C++ signature :  void press_current_dialog_button(TPyHandle<ASongApp>,int)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: int
            """
            pass

        def remove_control_surfaces_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "control_surfaces". C++ signature :  void remove_control_surfaces_listener(TPyHandle<ASongApp>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_open_dialog_count_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "open_dialog_count". C++ signature :  void remove_open_dialog_count_listener(TPyHandle<ASongApp>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_unavailable_features_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "unavailable_features". C++ signature :  void remove_unavailable_features_listener(TPyHandle<ASongApp>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def unavailable_features_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "unavailable_features". C++ signature :  bool unavailable_features_has_listener(TPyHandle<ASongApp>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Application
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                This class represents the view aspects of the Live application.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def browse_mode(self):
                """
                Return true if HotSwap mode is active for any target.
                """
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the application view.
                """
                pass

            @property
            def focused_document_view(self):
                """
                Return the name of the document view ('Session' or 'Arranger')shown in the currently selected window.
                """
                pass

            def add_browse_mode_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "browse_mode" has changed. C++ signature :  void add_browse_mode_listener(TPyViewData<ASongApp>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_focused_document_view_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "focused_document_view" has changed. C++ signature :  void add_focused_document_view_listener(TPyViewData<ASongApp>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_is_view_visible_listener(self, arg1, arg2, arg3):
                """
                Add a listener function or method, which will be called as soon as the property "is_view_visible" has changed. C++ signature :  void add_is_view_visible_listener(TPyViewData<ASongApp>,TString,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :param arg3: arg3
                :type arg3: object
                """
                pass

            def add_view_focus_changed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "view_focus_changed" has changed. C++ signature :  void add_view_focus_changed_listener(TPyViewData<ASongApp>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def available_main_views(self, arg1):
                """
                Return a list of strings with the available subcomponent views, which is to be specified, when using the rest of this classes functions. A 'subcomponent view' is a main view component of a document view, like the Session view, the Arranger or Detailview and so on... C++ signature :  std::__1::vector<TString, std::__1::allocator<TString> > available_main_views(TPyViewData<ASongApp>)
                :param arg1: arg1
                :type arg1: View
                :rtype: StringVector
                """
                pass

            def browse_mode_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "browse_mode". C++ signature :  bool browse_mode_has_listener(TPyViewData<ASongApp>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def focus_view(self, arg1, arg2):
                """
                Show and focus one through the identifier string specified view. C++ signature :  void focus_view(TPyViewData<ASongApp>,TString)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def focused_document_view_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "focused_document_view". C++ signature :  bool focused_document_view_has_listener(TPyViewData<ASongApp>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def hide_view(self, arg1, arg2):
                """
                Hide one through the identifier string specified view. C++ signature :  void hide_view(TPyViewData<ASongApp>,TString)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def is_view_visible(self, arg1, identifier, main_window_only=True):
                """
                Return true if the through the identifier string specified view is currently visible. If main_window_only is set to False, this will also check in second window. Notifications from the second window are not yet supported. C++ signature :  bool is_view_visible(TPyViewData<ASongApp>,TString [,bool=True])
                :param arg1: arg1
                :type arg1: View
                :param identifier: identifier
                :type identifier: object
                :param main_window_only: main_window_only defaults to True 
                :type main_window_only: bool
                :rtype: bool
                """
                pass

            def is_view_visible_has_listener(self, arg1, arg2, arg3):
                """
                Returns true, if the given listener function or method is connected to the property "is_view_visible". C++ signature :  bool is_view_visible_has_listener(TPyViewData<ASongApp>,TString,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :param arg3: arg3
                :type arg3: object
                :rtype: bool
                """
                pass

            def remove_browse_mode_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "browse_mode". C++ signature :  void remove_browse_mode_listener(TPyViewData<ASongApp>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_focused_document_view_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "focused_document_view". C++ signature :  void remove_focused_document_view_listener(TPyViewData<ASongApp>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_is_view_visible_listener(self, arg1, arg2, arg3):
                """
                Remove a previously set listener function or method from property "is_view_visible". C++ signature :  void remove_is_view_visible_listener(TPyViewData<ASongApp>,TString,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :param arg3: arg3
                :type arg3: object
                """
                pass

            def remove_view_focus_changed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "view_focus_changed". C++ signature :  void remove_view_focus_changed_listener(TPyViewData<ASongApp>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def scroll_view(self, arg1, arg2, arg3, arg4):
                """
                Scroll through the identifier string specified view into the given direction, if possible.  Will silently return if the specified view can not perform the requested action. C++ signature :  void scroll_view(TPyViewData<ASongApp>,int,TString,bool)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: int
                :param arg3: arg3
                :type arg3: object
                :param arg4: arg4
                :type arg4: bool
                """
                pass

            def show_view(self, arg1, arg2):
                """
                Show one through the identifier string specified view. Will throw a runtime error if this is called in Live's initialization scope. C++ signature :  void show_view(TPyViewData<ASongApp>,TString)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def toggle_browse(self, arg1):
                """
                Reveals the device chain, the browser and starts hot swap for the selected device. Calling this function again stops hot swap. C++ signature :  void toggle_browse(TPyViewData<ASongApp>)
                :param arg1: arg1
                :type arg1: View
                """
                pass

            def view_focus_changed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "view_focus_changed". C++ signature :  bool view_focus_changed_has_listener(TPyViewData<ASongApp>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def zoom_view(self, arg1, arg2, arg3, arg4):
                """
                Zoom through the identifier string specified view into the given direction, if possible.  Will silently return if the specified view can not perform the requested action. C++ signature :  void zoom_view(TPyViewData<ASongApp>,int,TString,bool)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: int
                :param arg3: arg3
                :type arg3: object
                :param arg4: arg4
                :type arg4: bool
                """
                pass

            class NavDirection(object):
                def __init__(self, *a, *k):
                    pass

                @property
                def down(self):
                    pass

                @property
                def left(self):
                    pass

                @property
                def right(self):
                    pass

                @property
                def up(self):
                    pass

    class UnavailableFeature(object):
        def __init__(self, *a, *k):
            pass

        @property
        def note_velocity_ranges_and_probabilities(self):
            pass

    class UnavailableFeatureVector(object):
        def __init__(self, *a, *k):
            """
            A container for returning unavailable features.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<NPythonApplication::TUnavailableFeature, std::__1::allocator<NPythonApplication::TUnavailableFeature> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: UnavailableFeatureVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<NPythonApplication::TUnavailableFeature, std::__1::allocator<NPythonApplication::TUnavailableFeature> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: UnavailableFeatureVector
            :param arg2: arg2
            :type arg2: object
            """
            pass


class Base(ModuleType):
    pass

    @staticmethod
    def log(arg1):
        """
        C++ signature :  void log(TString)
        :param arg1: arg1
        :type arg1: object
        """
        pass

    class FloatVector(object):
        def __init__(self, *a, *k):
            """
            A simple container for returning floats from Live.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<float, std::__1::allocator<float> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: FloatVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<float, std::__1::allocator<float> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: FloatVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

    class IntVector(object):
        def __init__(self, *a, *k):
            """
            A simple container for returning integers from Live.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<int, std::__1::allocator<int> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: IntVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<int, std::__1::allocator<int> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: IntVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

    class LimitationError(object):
        def __init__(self, *a, *k):
            pass

    class ObjectVector(object):
        def __init__(self, *a, *k):
            """
            A simple read only container for returning python objects.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<boost::python::api::object, std::__1::allocator<boost::python::api::object> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: ObjectVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<boost::python::api::object, std::__1::allocator<boost::python::api::object> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: ObjectVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

    class StringVector(object):
        def __init__(self, *a, *k):
            """
            A simple container for returning strings from Live.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<TString, std::__1::allocator<TString> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: StringVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<TString, std::__1::allocator<TString> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: StringVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

    class Timer(object):
        def __init__(self, *a, *k):
            """
            A timer that will trigger a callback after a certain inverval. The timer can be repeated and will trigger the callback every interval. Errors in the callback will stop the timer.
            """
            pass

        @property
        def running(self):
            pass

        def restart(self, arg1):
            """
            C++ signature :  void restart(PythonTimer {lvalue})
            :param arg1: arg1
            :type arg1: Timer
            """
            pass

        def start(self, arg1):
            """
            C++ signature :  void start(PythonTimer {lvalue})
            :param arg1: arg1
            :type arg1: Timer
            """
            pass

        def stop(self, arg1):
            """
            C++ signature :  void stop(PythonTimer {lvalue})
            :param arg1: arg1
            :type arg1: Timer
            """
            pass

    class Vector(object):
        def __init__(self, *a, *k):
            """
            A simple read only container for returning objects from Live.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<TWeakPtr<TPyHandleBase>, std::__1::allocator<TWeakPtr<TPyHandleBase> > > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: Vector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<TWeakPtr<TPyHandleBase>, std::__1::allocator<TWeakPtr<TPyHandleBase> > > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: Vector
            :param arg2: arg2
            :type arg2: object
            """
            pass


class Browser(ModuleType):
    pass

    class Browser(object):
        def __init__(self, *a, *k):
            """
            This class represents the live browser data base.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def audio_effects(self):
            """
            Returns a browser item with access to all the Audio Effects content.
            """
            pass

        @property
        def clips(self):
            """
            Returns a browser item with access to all the Clips content.
            """
            pass

        @property
        def colors(self):
            """
            Returns a list of browser items containing the configured colors.
            """
            pass

        @property
        def current_project(self):
            """
            Returns a browser item with access to all the Current Project content.
            """
            pass

        @property
        def drums(self):
            """
            Returns a browser item with access to all the Drums content.
            """
            pass

        @property
        def filter_type(self):
            """
            Bang triggered when the hotswap target has changed.
            """
            pass

        @property
        def hotswap_target(self):
            """
            Bang triggered when the hotswap target has changed.
            """
            pass

        @property
        def instruments(self):
            """
            Returns a browser item with access to all the Instruments content.
            """
            pass

        @property
        def legacy_libraries(self):
            """
            Returns a list of browser items containing the installed legacy libraries. The list is always empty as legacy library handling has been removed.
            """
            pass

        @property
        def max_for_live(self):
            """
            Returns a browser item with access to all the Max For Live content.
            """
            pass

        @property
        def midi_effects(self):
            """
            Returns a browser item with access to all the Midi Effects content.
            """
            pass

        @property
        def packs(self):
            """
            Returns a browser item with access to all the Packs content.
            """
            pass

        @property
        def plugins(self):
            """
            Returns a browser item with access to all the Plugins content.
            """
            pass

        @property
        def samples(self):
            """
            Returns a browser item with access to all the Samples content.
            """
            pass

        @property
        def sounds(self):
            """
            Returns a browser item with access to all the Sounds content.
            """
            pass

        @property
        def user_folders(self):
            """
            Returns a list of browser items containing all the user folders.
            """
            pass

        @property
        def user_library(self):
            """
            Returns a browser item with access to all the User Library content.
            """
            pass

        def add_filter_type_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "filter_type" has changed. C++ signature :  void add_filter_type_listener(TPyHandle<ABrowserDelegate>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_full_refresh_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "full_refresh" has changed. C++ signature :  void add_full_refresh_listener(TPyHandle<ABrowserDelegate>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_hotswap_target_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "hotswap_target" has changed. C++ signature :  void add_hotswap_target_listener(TPyHandle<ABrowserDelegate>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def filter_type_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "filter_type". C++ signature :  bool filter_type_has_listener(TPyHandle<ABrowserDelegate>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def full_refresh_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "full_refresh". C++ signature :  bool full_refresh_has_listener(TPyHandle<ABrowserDelegate>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def hotswap_target_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "hotswap_target". C++ signature :  bool hotswap_target_has_listener(TPyHandle<ABrowserDelegate>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def load_item(self, arg1, arg2):
            """
            Loads the provided browser item. C++ signature :  void load_item(TPyHandle<ABrowserDelegate>,NPythonBrowser::TPythonBrowserItem)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: BrowserItem
            """
            pass

        def preview_item(self, arg1, arg2):
            """
            Previews the provided browser item. C++ signature :  void preview_item(TPyHandle<ABrowserDelegate>,NPythonBrowser::TPythonBrowserItem)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: BrowserItem
            """
            pass

        def relation_to_hotswap_target(self, arg1, arg2):
            """
            Returns the relation between the given browser item and the current hotswap target C++ signature :  NBrowserUri::TRelation relation_to_hotswap_target(TPyHandle<ABrowserDelegate>,NPythonBrowser::TPythonBrowserItem)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: BrowserItem
            :rtype: Relation
            """
            pass

        def remove_filter_type_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "filter_type". C++ signature :  void remove_filter_type_listener(TPyHandle<ABrowserDelegate>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_full_refresh_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "full_refresh". C++ signature :  void remove_full_refresh_listener(TPyHandle<ABrowserDelegate>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_hotswap_target_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "hotswap_target". C++ signature :  void remove_hotswap_target_listener(TPyHandle<ABrowserDelegate>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Browser
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def stop_preview(self, arg1):
            """
            Stop the current preview. C++ signature :  void stop_preview(TPyHandle<ABrowserDelegate>)
            :param arg1: arg1
            :type arg1: Browser
            """
            pass

    class BrowserItem(object):
        def __init__(self, *a, *k):
            """
            This class represents an item of the browser hierarchy.
            """
            pass

        @property
        def children(self):
            """
            Const access to the descendants of this browser item.
            """
            pass

        @property
        def is_device(self):
            """
            Indicates if the browser item represents a device.
            """
            pass

        @property
        def is_folder(self):
            """
            Indicates if the browser item represents folder.
            """
            pass

        @property
        def is_loadable(self):
            """
            True if item can be loaded via the Browser's 'load_item' method.
            """
            pass

        @property
        def is_selected(self):
            """
            True if the item is ancestor of or the actual selection.
            """
            pass

        @property
        def iter_children(self):
            """
            Const iterable access to the descendants of this browser item.
            """
            pass

        @property
        def name(self):
            """
            Const access to the canonical display name of this browser item.
            """
            pass

        @property
        def source(self):
            """
            Specifies where does item come from -- i.e. Live pack, user library...
            """
            pass

        @property
        def uri(self):
            """
            The uri describes a unique identifier for a browser item.
            """
            pass

    class BrowserItemIterator(object):
        def __init__(self, *a, *k):
            """
            This class iterates over children of another BrowserItem.
            """
            pass

        def next(self, arg1):
            """
            Retrieve next item C++ signature :  NPythonBrowser::TPythonBrowserItem next(NPythonBrowser::TPythonBrowserItem::TPythonBrowserItemIterator {lvalue})
            :param arg1: arg1
            :type arg1: BrowserItemIterator
            :rtype: BrowserItem
            """
            pass

    class BrowserItemVector(object):
        def __init__(self, *a, *k):
            """
            A container for returning browser items from Live.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<NPythonBrowser::TPythonBrowserItem, std::__1::allocator<NPythonBrowser::TPythonBrowserItem> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: BrowserItemVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<NPythonBrowser::TPythonBrowserItem, std::__1::allocator<NPythonBrowser::TPythonBrowserItem> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: BrowserItemVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

    class FilterType(object):
        def __init__(self, *a, *k):
            pass

        @property
        def audio_effect_hotswap(self):
            pass

        @property
        def count(self):
            pass

        @property
        def disabled(self):
            pass

        @property
        def drum_pad_hotswap(self):
            pass

        @property
        def hotswap_off(self):
            pass

        @property
        def instrument_hotswap(self):
            pass

        @property
        def midi_effect_hotswap(self):
            pass

        @property
        def midi_track_devices(self):
            pass

        @property
        def samples(self):
            pass

    class Relation(object):
        def __init__(self, *a, *k):
            pass

        @property
        def ancestor(self):
            pass

        @property
        def descendant(self):
            pass

        @property
        def equal(self):
            pass

        @property
        def none(self):
            pass


class Chain(ModuleType):
    pass

    class Chain(object):
        def __init__(self, *a, *k):
            """
            This class represents a group device chain in Live.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the chain.
            """
            pass

        @property
        def color(self):
            """
            Access the color index of the Chain.
            """
            pass

        @property
        def color_index(self):
            """
            Access the color index of the Chain.
            """
            pass

        @property
        def devices(self):
            """
            Return const access to all available Devices that are present in the chains
            """
            pass

        @property
        def has_audio_input(self):
            """
            return True, if this Chain can be feed with an Audio signal. This istrue for all Audio Chains.
            """
            pass

        @property
        def has_audio_output(self):
            """
            return True, if this Chain sends out an Audio signal. This istrue for all Audio Chains, and MIDI chains with an Instrument.
            """
            pass

        @property
        def has_midi_input(self):
            """
            return True, if this Chain can be feed with an Audio signal. This istrue for all MIDI Chains.
            """
            pass

        @property
        def has_midi_output(self):
            """
            return True, if this Chain sends out MIDI events. This istrue for all MIDI Chains with no Instruments.
            """
            pass

        @property
        def is_auto_colored(self):
            """
            Get/set access to the auto color flag of the Chain.If True, the Chain will always have the same color as the containingTrack or Chain.
            """
            pass

        @property
        def mixer_device(self):
            """
            Return access to the mixer device that holds the chain's mixer parameters:the Volume, Pan, and Sendamounts.
            """
            pass

        @property
        def mute(self):
            """
            Mute/unmute the chain.
            """
            pass

        @property
        def muted_via_solo(self):
            """
            Return const access to whether this chain is muted due to some other chainbeing soloed.
            """
            pass

        @property
        def name(self):
            """
            Read/write access to the name of the Chain, as visible in the track header.
            """
            pass

        @property
        def solo(self):
            """
            Get/Set the solo status of the chain. Note that this will not disable thesolo state of any other Chain in the same rack. If you want exclusive solo, you have to disable the solo state of the other Chains manually.
            """
            pass

        def add_color_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color_index" has changed. C++ signature :  void add_color_index_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_color_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color" has changed. C++ signature :  void add_color_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_devices_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "devices" has changed. C++ signature :  void add_devices_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_auto_colored_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_auto_colored" has changed. C++ signature :  void add_is_auto_colored_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_mute_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "mute" has changed. C++ signature :  void add_mute_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_muted_via_solo_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "muted_via_solo" has changed. C++ signature :  void add_muted_via_solo_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_solo_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "solo" has changed. C++ signature :  void add_solo_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def color_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color". C++ signature :  bool color_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def color_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color_index". C++ signature :  bool color_index_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def delete_device(self, arg1, arg2):
            """
            Remove a device identified by its index from the chain. Throws runtime error if bad index.  C++ signature :  void delete_device(TChainPyHandle,int)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: int
            """
            pass

        def devices_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "devices". C++ signature :  bool devices_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_auto_colored_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_auto_colored". C++ signature :  bool is_auto_colored_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def mute_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "mute". C++ signature :  bool mute_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def muted_via_solo_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "muted_via_solo". C++ signature :  bool muted_via_solo_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_color_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color_index". C++ signature :  void remove_color_index_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_color_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color". C++ signature :  void remove_color_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_devices_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "devices". C++ signature :  void remove_devices_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_auto_colored_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_auto_colored". C++ signature :  void remove_is_auto_colored_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_mute_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "mute". C++ signature :  void remove_mute_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_muted_via_solo_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "muted_via_solo". C++ signature :  void remove_muted_via_solo_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_solo_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "solo". C++ signature :  void remove_solo_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def solo_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "solo". C++ signature :  bool solo_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass


class ChainMixerDevice(ModuleType):
    pass

    class ChainMixerDevice(object):
        def __init__(self, *a, *k):
            """
            This class represents a Chain's Mixer Device in Live, which gives youaccess to the Volume, Panning, and Send properties of a Chain.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the mixer device.
            """
            pass

        @property
        def chain_activator(self):
            """
            Const access to the Chain's Activator Device Parameter.
            """
            pass

        @property
        def panning(self):
            """
            Const access to the Chain's Panning Device Parameter.
            """
            pass

        @property
        def sends(self):
            """
            Const access to the Chain's list of Send Amount Device Parameters.
            """
            pass

        @property
        def volume(self):
            """
            Const access to the Chain's Volume Device Parameter.
            """
            pass

        def add_sends_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "sends" has changed. C++ signature :  void add_sends_listener(TPyHandle<ABranchMixerDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ChainMixerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_sends_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "sends". C++ signature :  void remove_sends_listener(TPyHandle<ABranchMixerDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ChainMixerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def sends_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "sends". C++ signature :  bool sends_has_listener(TPyHandle<ABranchMixerDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ChainMixerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass


class Clip(ModuleType):
    pass

    class AutomationEnvelope(object):
        def __init__(self, *a, *k):
            """
            Describes parameter automation per clip.
            """
            pass

        def insert_step(self, arg1, arg2, arg3, arg4):
            """
            C++ signature :  void insert_step(AAutomation {lvalue},double,double,double)
            :param arg1: arg1
            :type arg1: AutomationEnvelope
            :param arg2: arg2
            :type arg2: float
            :param arg3: arg3
            :type arg3: float
            :param arg4: arg4
            :type arg4: float
            """
            pass

        def value_at_time(self, arg1, arg2):
            """
            C++ signature :  double value_at_time(AAutomation {lvalue},double)
            :param arg1: arg1
            :type arg1: AutomationEnvelope
            :param arg2: arg2
            :type arg2: float
            :rtype: float
            """
            pass

    class Clip(object):
        def __init__(self, *a, *k):
            """
            This class represents a Clip in Live. It can be either an AudioClip or a MIDI Clip, in an Arrangement or the Session, dependingon the Track (Slot) it lives in.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def available_warp_modes(self):
            """
            Available for AudioClips only.Get/Set the available warp modes, that can be used.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Clip.
            """
            pass

        @property
        def color(self):
            """
            Get/set access to the color of the Clip (RGB).
            """
            pass

        @property
        def color_index(self):
            """
            Get/set access to the color index of the Clip.
            """
            pass

        @property
        def end_marker(self):
            """
            Get/Set the Clips end marker pos in beats/seconds (unit depends on warping).
            """
            pass

        @property
        def end_time(self):
            """
            Get the clip's end time.
            """
            pass

        @property
        def file_path(self):
            """
            Get the path of the file represented by the Audio Clip.
            """
            pass

        @property
        def gain(self):
            """
            Available for AudioClips only.Read/write access to the gain setting of theAudio Clip
            """
            pass

        @property
        def gain_display_string(self):
            """
            Return a string with the gain as dB value
            """
            pass

        @property
        def groove(self):
            """
            Get the groove associated with this clip.
            """
            pass

        @property
        def has_envelopes(self):
            """
            Will notify if the clip gets his first envelope or the last envelope is removed.
            """
            pass

        @property
        def has_groove(self):
            """
            Returns true if a groove is associated with this clip.
            """
            pass

        @property
        def is_arrangement_clip(self):
            """
            return true if this Clip is an Arrangement Clip.A Clip can be either a Session or Arrangement Clip.
            """
            pass

        @property
        def is_audio_clip(self):
            """
            Return true if this Clip is an Audio Clip.A Clip can be either an Audioclip or a MIDI Clip.
            """
            pass

        @property
        def is_midi_clip(self):
            """
            return true if this Clip is a MIDI Clip.A Clip can be either an Audioclip or a MIDI Clip.
            """
            pass

        @property
        def is_overdubbing(self):
            """
            returns true if the Clip is recording overdubs
            """
            pass

        @property
        def is_playing(self):
            """
            Get/Set if this Clip is currently playing. If the Clips trigger modeis set to a quantization value, the Clip will not start playing immediately.If you need to know wether the Clip was triggered, use the is_triggered property.
            """
            pass

        @property
        def is_recording(self):
            """
            returns true if the Clip was triggered to record or is recording.
            """
            pass

        @property
        def is_triggered(self):
            """
            returns true if the Clip was triggered or is playing.
            """
            pass

        @property
        def launch_mode(self):
            """
            Get/Set access to the launch mode setting of the Clip.
            """
            pass

        @property
        def launch_quantization(self):
            """
            Get/Set access to the launch quantization setting of the Clip.
            """
            pass

        @property
        def legato(self):
            """
            Get/Set access to the legato setting of the Clip
            """
            pass

        @property
        def length(self):
            """
            Get to the Clips length in beats/seconds (unit depends on warping).
            """
            pass

        @property
        def loop_end(self):
            """
            Get/Set the loop end pos of this Clip in beats/seconds (unit depends on warping).
            """
            pass

        @property
        def loop_start(self):
            """
            Get/Set the Clips loopstart pos in beats/seconds (unit depends on warping).
            """
            pass

        @property
        def looping(self):
            """
            Get/Set the Clips 'loop is enabled' flag.Only Warped Audio Clips or MIDI Clip can be looped.
            """
            pass

        @property
        def muted(self):
            """
            Read/write access to the mute state of the Clip.
            """
            pass

        @property
        def name(self):
            """
            Read/write access to the name of the Clip.
            """
            pass

        @property
        def pitch_coarse(self):
            """
            Available for AudioClips only.Read/write access to the pitch (in halftones) setting of theAudio Clip, ranging from -48 to 48
            """
            pass

        @property
        def pitch_fine(self):
            """
            Available for AudioClips only.Read/write access to the pitch fine setting of theAudio Clip, ranging from -500 to 500
            """
            pass

        @property
        def playing_position(self):
            """
            Constant access to the current playing position of the clip.The returned value is the position in beats for midi and warped audio clips,or in seconds for unwarped audio clips. Stopped clips will return 0.
            """
            pass

        @property
        def position(self):
            """
            Get/Set the loop position of this Clip in beats/seconds (unit depends on warping).
            """
            pass

        @property
        def ram_mode(self):
            """
            Available for AudioClips only.Read/write access to the Ram mode setting of the Audio Clip
            """
            pass

        @property
        def sample_length(self):
            """
            Available for AudioClips only.Get the sample length in sample time or -1 if there is no sample available.
            """
            pass

        @property
        def signature_denominator(self):
            """
            Get/Set access to the global signature denominator of the Clip.
            """
            pass

        @property
        def signature_numerator(self):
            """
            Get/Set access to the global signature numerator of the Clip.
            """
            pass

        @property
        def start_marker(self):
            """
            Get/Set the Clips start marker pos in beats/seconds (unit depends on warping).
            """
            pass

        @property
        def start_time(self):
            """
            Get the clip's start time offset. For Session View clips, this is the time the clip was started. For Arrangement View clips, this is the offset within the arrangement.
            """
            pass

        @property
        def velocity_amount(self):
            """
            Get/Set access to the velocity to volume amount of the Clip.
            """
            pass

        @property
        def view(self):
            """
            Get the view of the Clip.
            """
            pass

        @property
        def warp_markers(self):
            """
            Available for AudioClips only.Get the warp markers for this audio clip.
            """
            pass

        @property
        def warp_mode(self):
            """
            Available for AudioClips only.Get/Set the warp mode for this audio clip.
            """
            pass

        @property
        def warping(self):
            """
            Available for AudioClips only.Get/Set if this Clip is timestreched.
            """
            pass

        @property
        def will_record_on_start(self):
            """
            returns true if the Clip will record on being started.
            """
            pass

        def add_color_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color_index" has changed. C++ signature :  void add_color_index_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_color_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color" has changed. C++ signature :  void add_color_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_end_marker_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "end_marker" has changed. C++ signature :  void add_end_marker_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_end_time_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "end_time" has changed. C++ signature :  void add_end_time_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_file_path_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "file_path" has changed. C++ signature :  void add_file_path_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_gain_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "gain" has changed. C++ signature :  void add_gain_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_groove_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "groove" has changed. C++ signature :  void add_groove_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_has_envelopes_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "has_envelopes" has changed. C++ signature :  void add_has_envelopes_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_overdubbing_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_overdubbing" has changed. C++ signature :  void add_is_overdubbing_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_recording_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_recording" has changed. C++ signature :  void add_is_recording_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_launch_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "launch_mode" has changed. C++ signature :  void add_launch_mode_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_launch_quantization_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "launch_quantization" has changed. C++ signature :  void add_launch_quantization_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_legato_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "legato" has changed. C++ signature :  void add_legato_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_loop_end_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "loop_end" has changed. C++ signature :  void add_loop_end_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_loop_jump_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "loop_jump" has changed. C++ signature :  void add_loop_jump_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_loop_start_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "loop_start" has changed. C++ signature :  void add_loop_start_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_looping_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "looping" has changed. C++ signature :  void add_looping_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_muted_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "muted" has changed. C++ signature :  void add_muted_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_new_notes(self, arg1, arg2):
            """
            Expects a Python iterable holding a number of Live.Clip.MidiNoteSpecification objects. The objects will be used to construct new notes in the clip. C++ signature :  void add_new_notes(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_notes_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "notes" has changed. C++ signature :  void add_notes_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_pitch_coarse_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "pitch_coarse" has changed. C++ signature :  void add_pitch_coarse_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_pitch_fine_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "pitch_fine" has changed. C++ signature :  void add_pitch_fine_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_playing_position_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "playing_position" has changed. C++ signature :  void add_playing_position_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_playing_status_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "playing_status" has changed. C++ signature :  void add_playing_status_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_position_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "position" has changed. C++ signature :  void add_position_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_ram_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "ram_mode" has changed. C++ signature :  void add_ram_mode_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_signature_denominator_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "signature_denominator" has changed. C++ signature :  void add_signature_denominator_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_signature_numerator_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "signature_numerator" has changed. C++ signature :  void add_signature_numerator_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_start_marker_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "start_marker" has changed. C++ signature :  void add_start_marker_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_velocity_amount_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "velocity_amount" has changed. C++ signature :  void add_velocity_amount_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_warp_markers_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "warp_markers" has changed. C++ signature :  void add_warp_markers_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_warp_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "warp_mode" has changed. C++ signature :  void add_warp_mode_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_warping_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "warping" has changed. C++ signature :  void add_warping_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def apply_note_modifications(self, arg1, arg2):
            """
            Expects a list of notes as returned from get_notes_extended. The content of the list will be used to modify existing notes in the clip, based on matching note IDs. This function should be used when modifying existing notes, e.g. changing the velocity or start time. The function ensures that per-note events attached to the modified notes are preserved. This is NOT the case when replacing notes via a combination of remove_notes_extended and add_new_notes. The given list can be a subset of the notes in the clip, but it must not contain any notes that are not present in the clip.  C++ signature :  void apply_note_modifications(TPyHandle<AClip>,std::__1::vector<NClipApi::TNoteInfo, std::__1::allocator<NClipApi::TNoteInfo> >)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: MidiNoteVector
            """
            pass

        def automation_envelope(self, arg1, arg2):
            """
            Return the envelope for the given parameter.Returns None if the envelope doesn't exist.Returns None for Arrangement clips.Returns None for parameters from a different track. C++ signature :  TWeakPtr<AAutomation> automation_envelope(TPyHandle<AClip>,TPyHandle<ATimeableValue>)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: DeviceParameter
            :rtype: AutomationEnvelope
            """
            pass

        def beat_to_sample_time(self, handle, beat_time):
            """
            Available for AudioClips only. Converts the given beat time to sample time. Raises an error if the sample is not warped. C++ signature :  double beat_to_sample_time(TPyHandle<AClip>,double)
            :param handle: handle
            :type handle: Clip
            :param beat_time: beat_time
            :type beat_time: float
            :rtype: float
            """
            pass

        def clear_all_envelopes(self, arg1):
            """
            Clears all envelopes for this clip. C++ signature :  void clear_all_envelopes(TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Clip
            """
            pass

        def clear_envelope(self, arg1, arg2):
            """
            Clears the envelope of this clips given parameter. C++ signature :  void clear_envelope(TPyHandle<AClip>,TPyHandle<ATimeableValue>)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: DeviceParameter
            """
            pass

        def color_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color". C++ signature :  bool color_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def color_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color_index". C++ signature :  bool color_index_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def create_automation_envelope(self, arg1, arg2):
            """
            Creates an envelope for a given parameter and returns it.This should only be used if the envelope doesn't exist.Raises an error if the envelope can't be created. C++ signature :  TWeakPtr<AAutomation> create_automation_envelope(TPyHandle<AClip>,TPyHandle<ATimeableValue>)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: DeviceParameter
            :rtype: AutomationEnvelope
            """
            pass

        def crop(self, arg1):
            """
            Crops the clip. The region that is cropped depends on whether the clip is looped or not. If looped, the region outside of the loop is removed. If not looped, the region outside the start and end markers is removed. C++ signature :  void crop(TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Clip
            """
            pass

        def deselect_all_notes(self, arg1):
            """
            De-selects all notes present in the clip. C++ signature :  void deselect_all_notes(TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Clip
            """
            pass

        def duplicate_loop(self, arg1):
            """
            Make the loop two times longer and duplicates notes and envelopes. Duplicates the clip start/end range if the clip is not looped. C++ signature :  void duplicate_loop(TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Clip
            """
            pass

        def duplicate_region(self, handle, region_start, region_length, destination_time, pitch=-1, transposition_amount=0):
            """
            Duplicate the notes in the specified region to the destination_time. Only notes of the specified pitch are duplicated or all if pitch is -1. If the transposition_amount is not 0, the notes in the region will be transposed by the transpose_amount of semitones.Raises an error on audio clips. C++ signature :  void duplicate_region(TPyHandle<AClip>,double,double,double [,int=-1 [,int=0]])
            :param handle: handle
            :type handle: Clip
            :param region_start: region_start
            :type region_start: float
            :param region_length: region_length
            :type region_length: float
            :param destination_time: destination_time
            :type destination_time: float
            :param pitch: pitch defaults to -1 
            :type pitch: int
            :param transposition_amount: transposition_amount defaults to 0 
            :type transposition_amount: int
            """
            pass

        def end_marker_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "end_marker". C++ signature :  bool end_marker_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def end_time_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "end_time". C++ signature :  bool end_time_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def file_path_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "file_path". C++ signature :  bool file_path_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def fire(self, arg1):
            """
            (Re)Start playing this Clip. C++ signature :  void fire(TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Clip
            """
            pass

        def gain_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "gain". C++ signature :  bool gain_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def get_notes(self, handle, from_time, from_pitch, time_span, pitch_span):
            """
            Returns a tuple of tuples where each inner tuple represents a note starting in the given pitch- and time range. The inner tuple contains pitch, time, duration, velocity, and mute state. C++ signature :  boost::python::tuple get_notes(TPyHandle<AClip>,double,int,double,int)
            :param handle: handle
            :type handle: Clip
            :param from_time: from_time
            :type from_time: float
            :param from_pitch: from_pitch
            :type from_pitch: int
            :param time_span: time_span
            :type time_span: float
            :param pitch_span: pitch_span
            :type pitch_span: int
            :rtype: tuple
            """
            pass

        def get_notes_by_id(self, arg1, arg2):
            """
            Return a list of MIDI notes matching the given note IDs.  C++ signature :  std::__1::vector<NClipApi::TNoteInfo, std::__1::allocator<NClipApi::TNoteInfo> > get_notes_by_id(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: MidiNoteVector
            """
            pass

        def get_notes_extended(self, arg1, from_pitch, pitch_span, from_time, time_span):
            """
            Returns a list of MIDI notes from the given pitch and time range. Each note is represented by a Live.Clip.MidiNote object. The returned list can be modified freely, but modifications will not be reflected in the MIDI clip until apply_note_modifications is called. C++ signature :  std::__1::vector<NClipApi::TNoteInfo, std::__1::allocator<NClipApi::TNoteInfo> > get_notes_extended(TPyHandle<AClip>,int,int,double,double)
            :param arg1: arg1
            :type arg1: Clip
            :param from_pitch: from_pitch
            :type from_pitch: int
            :param pitch_span: pitch_span
            :type pitch_span: int
            :param from_time: from_time
            :type from_time: float
            :param time_span: time_span
            :type time_span: float
            :rtype: MidiNoteVector
            """
            pass

        def get_selected_notes(self, arg1):
            """
            Returns a tuple of tuples where each inner tuple represents a selected note. The inner tuple contains pitch, time, duration, velocity, and mute state. C++ signature :  boost::python::tuple get_selected_notes(TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Clip
            :rtype: tuple
            """
            pass

        def get_selected_notes_extended(self, arg1):
            """
            Returns a list of all MIDI notes from the clip that are currently selected. Each note is represented by a Live.Clip.MidiNote object. The returned list can be modified freely, but modifications will not be reflected in the MIDI clip until apply_note_modifications is called. C++ signature :  std::__1::vector<NClipApi::TNoteInfo, std::__1::allocator<NClipApi::TNoteInfo> > get_selected_notes_extended(TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Clip
            :rtype: MidiNoteVector
            """
            pass

        def groove_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "groove". C++ signature :  bool groove_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def has_envelopes_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "has_envelopes". C++ signature :  bool has_envelopes_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_overdubbing_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_overdubbing". C++ signature :  bool is_overdubbing_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_recording_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_recording". C++ signature :  bool is_recording_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def launch_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "launch_mode". C++ signature :  bool launch_mode_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def launch_quantization_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "launch_quantization". C++ signature :  bool launch_quantization_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def legato_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "legato". C++ signature :  bool legato_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def loop_end_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "loop_end". C++ signature :  bool loop_end_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def loop_jump_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "loop_jump". C++ signature :  bool loop_jump_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def loop_start_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "loop_start". C++ signature :  bool loop_start_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def looping_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "looping". C++ signature :  bool looping_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def move_playing_pos(self, arg1, arg2):
            """
            Jump forward or backward by the specified relative amount in beats. Will do nothing, if the Clip is not playing. C++ signature :  void move_playing_pos(TPyHandle<AClip>,double)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: float
            """
            pass

        def muted_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "muted". C++ signature :  bool muted_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def notes_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "notes". C++ signature :  bool notes_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def pitch_coarse_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "pitch_coarse". C++ signature :  bool pitch_coarse_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def pitch_fine_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "pitch_fine". C++ signature :  bool pitch_fine_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def playing_position_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "playing_position". C++ signature :  bool playing_position_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def playing_status_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "playing_status". C++ signature :  bool playing_status_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def position_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "position". C++ signature :  bool position_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def quantize(self, arg1, arg2, arg3):
            """
            Quantize all notes in a clip or align warp markers. C++ signature :  void quantize(TPyHandle<AClip>,int,float)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: float
            """
            pass

        def quantize_pitch(self, arg1, arg2, arg3, arg4):
            """
            Quantize all the notes of a given pitch.  Raises an error on audio clips. C++ signature :  void quantize_pitch(TPyHandle<AClip>,int,int,float)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            :param arg4: arg4
            :type arg4: float
            """
            pass

        def ram_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "ram_mode". C++ signature :  bool ram_mode_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_color_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color_index". C++ signature :  void remove_color_index_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_color_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color". C++ signature :  void remove_color_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_end_marker_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "end_marker". C++ signature :  void remove_end_marker_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_end_time_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "end_time". C++ signature :  void remove_end_time_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_file_path_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "file_path". C++ signature :  void remove_file_path_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_gain_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "gain". C++ signature :  void remove_gain_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_groove_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "groove". C++ signature :  void remove_groove_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_has_envelopes_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "has_envelopes". C++ signature :  void remove_has_envelopes_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_overdubbing_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_overdubbing". C++ signature :  void remove_is_overdubbing_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_recording_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_recording". C++ signature :  void remove_is_recording_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_launch_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "launch_mode". C++ signature :  void remove_launch_mode_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_launch_quantization_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "launch_quantization". C++ signature :  void remove_launch_quantization_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_legato_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "legato". C++ signature :  void remove_legato_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_loop_end_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "loop_end". C++ signature :  void remove_loop_end_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_loop_jump_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "loop_jump". C++ signature :  void remove_loop_jump_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_loop_start_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "loop_start". C++ signature :  void remove_loop_start_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_looping_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "looping". C++ signature :  void remove_looping_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_muted_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "muted". C++ signature :  void remove_muted_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_notes(self, arg1, arg2, arg3, arg4, arg5):
            """
            Delete all notes starting in the given pitch- and time range. C++ signature :  void remove_notes(TPyHandle<AClip>,double,int,double,int)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: float
            :param arg3: arg3
            :type arg3: int
            :param arg4: arg4
            :type arg4: float
            :param arg5: arg5
            :type arg5: int
            """
            pass

        def remove_notes_by_id(self, arg1, arg2):
            """
            Delete all notes matching the given note IDs. This function should NOT be used to implement modification of existing notes (i.e. in combination with add_new_notes), as that leads to loss of per-note events. apply_note_modifications must be used instead for modifying existing notes. C++ signature :  void remove_notes_by_id(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_notes_extended(self, arg1, from_pitch, pitch_span, from_time, time_span):
            """
            Delete all notes starting in the given pitch and time range. This function should NOT be used to implement modification of existing notes (i.e. in combination with add_new_notes), as that leads to loss of per-note events. apply_note_modifications must be used instead for modifying existing notes. C++ signature :  void remove_notes_extended(TPyHandle<AClip>,int,int,double,double)
            :param arg1: arg1
            :type arg1: Clip
            :param from_pitch: from_pitch
            :type from_pitch: int
            :param pitch_span: pitch_span
            :type pitch_span: int
            :param from_time: from_time
            :type from_time: float
            :param time_span: time_span
            :type time_span: float
            """
            pass

        def remove_notes_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "notes". C++ signature :  void remove_notes_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_pitch_coarse_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "pitch_coarse". C++ signature :  void remove_pitch_coarse_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_pitch_fine_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "pitch_fine". C++ signature :  void remove_pitch_fine_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_playing_position_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "playing_position". C++ signature :  void remove_playing_position_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_playing_status_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "playing_status". C++ signature :  void remove_playing_status_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_position_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "position". C++ signature :  void remove_position_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_ram_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "ram_mode". C++ signature :  void remove_ram_mode_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_signature_denominator_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "signature_denominator". C++ signature :  void remove_signature_denominator_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_signature_numerator_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "signature_numerator". C++ signature :  void remove_signature_numerator_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_start_marker_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "start_marker". C++ signature :  void remove_start_marker_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_velocity_amount_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "velocity_amount". C++ signature :  void remove_velocity_amount_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_warp_markers_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "warp_markers". C++ signature :  void remove_warp_markers_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_warp_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "warp_mode". C++ signature :  void remove_warp_mode_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_warping_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "warping". C++ signature :  void remove_warping_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def replace_selected_notes(self, arg1, arg2):
            """
            Called with a tuple of tuples where each inner tuple represents a note in the same format as returned by get_selected_notes. The notes described that way will then be used to replace the old selection. C++ signature :  void replace_selected_notes(TPyHandle<AClip>,boost::python::tuple)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: tuple
            """
            pass

        def sample_to_beat_time(self, handle, sample_time):
            """
            Available for AudioClips only. Converts the given sample time to beat time. Raises an error if the sample is not warped. C++ signature :  double sample_to_beat_time(TPyHandle<AClip>,double)
            :param handle: handle
            :type handle: Clip
            :param sample_time: sample_time
            :type sample_time: float
            :rtype: float
            """
            pass

        def scrub(self, handle, scrub_position):
            """
            Scrubs inside a clip. scrub_position defines the position in beats that the scrub will start from. The scrub will continue until stop_scrub is called. Global quantization applies to the scrub's position and length. C++ signature :  void scrub(TPyHandle<AClip>,double)
            :param handle: handle
            :type handle: Clip
            :param scrub_position: scrub_position
            :type scrub_position: float
            """
            pass

        def seconds_to_sample_time(self, handle, seconds):
            """
            Available for AudioClips only. Converts the given seconds to sample time. Raises an error if the sample is warped. C++ signature :  double seconds_to_sample_time(TPyHandle<AClip>,double)
            :param handle: handle
            :type handle: Clip
            :param seconds: seconds
            :type seconds: float
            :rtype: float
            """
            pass

        def select_all_notes(self, arg1):
            """
            Selects all notes present in the clip. C++ signature :  void select_all_notes(TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Clip
            """
            pass

        def set_fire_button_state(self, arg1, arg2):
            """
            Set the clip's fire button state directly. Supports all launch modes. C++ signature :  void set_fire_button_state(TPyHandle<AClip>,bool)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: bool
            """
            pass

        def set_notes(self, arg1, arg2):
            """
            Called with a tuple of tuples where each inner tuple represents a note in the same format as returned by get_notes. The notes described that way will then be added to the clip. C++ signature :  void set_notes(TPyHandle<AClip>,boost::python::tuple)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: tuple
            """
            pass

        def signature_denominator_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "signature_denominator". C++ signature :  bool signature_denominator_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def signature_numerator_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "signature_numerator". C++ signature :  bool signature_numerator_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def start_marker_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "start_marker". C++ signature :  bool start_marker_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def stop(self, arg1):
            """
            Stop playing this Clip. C++ signature :  void stop(TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Clip
            """
            pass

        def stop_scrub(self, arg1):
            """
            Stops the current scrub. C++ signature :  void stop_scrub(TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Clip
            """
            pass

        def velocity_amount_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "velocity_amount". C++ signature :  bool velocity_amount_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def warp_markers_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "warp_markers". C++ signature :  bool warp_markers_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def warp_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "warp_mode". C++ signature :  bool warp_mode_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def warping_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "warping". C++ signature :  bool warping_has_listener(TPyHandle<AClip>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Clip
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a Clip.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the clip view.
                """
                pass

            @property
            def grid_is_triplet(self):
                """
                Get/set wether the grid is showing in triplet mode.
                """
                pass

            @property
            def grid_quantization(self):
                """
                Get/set clip grid quantization resolution.
                """
                pass

            def hide_envelope(self, arg1):
                """
                Hide the envelope view. C++ signature :  void hide_envelope(TPyViewData<AClip>)
                :param arg1: arg1
                :type arg1: View
                """
                pass

            def select_envelope_parameter(self, arg1, arg2):
                """
                Select the given device parameter in the envelope view. C++ signature :  void select_envelope_parameter(TPyViewData<AClip>,TPyHandle<ATimeableValue>)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: DeviceParameter
                """
                pass

            def show_envelope(self, arg1):
                """
                Show the envelope view. C++ signature :  void show_envelope(TPyViewData<AClip>)
                :param arg1: arg1
                :type arg1: View
                """
                pass

            def show_loop(self, arg1):
                """
                Show the entire loop in the detail view. C++ signature :  void show_loop(TPyViewData<AClip>)
                :param arg1: arg1
                :type arg1: View
                """
                pass

    class ClipLaunchQuantization(object):
        def __init__(self, *a, *k):
            pass

        @property
        def q_2_bars(self):
            pass

        @property
        def q_4_bars(self):
            pass

        @property
        def q_8_bars(self):
            pass

        @property
        def q_bar(self):
            pass

        @property
        def q_eighth(self):
            pass

        @property
        def q_eighth_triplet(self):
            pass

        @property
        def q_global(self):
            pass

        @property
        def q_half(self):
            pass

        @property
        def q_half_triplet(self):
            pass

        @property
        def q_none(self):
            pass

        @property
        def q_quarter(self):
            pass

        @property
        def q_quarter_triplet(self):
            pass

        @property
        def q_sixteenth(self):
            pass

        @property
        def q_sixteenth_triplet(self):
            pass

        @property
        def q_thirtysecond(self):
            pass

    class GridQuantization(object):
        def __init__(self, *a, *k):
            pass

        @property
        def count(self):
            pass

        @property
        def g_2_bars(self):
            pass

        @property
        def g_4_bars(self):
            pass

        @property
        def g_8_bars(self):
            pass

        @property
        def g_bar(self):
            pass

        @property
        def g_eighth(self):
            pass

        @property
        def g_half(self):
            pass

        @property
        def g_quarter(self):
            pass

        @property
        def g_sixteenth(self):
            pass

        @property
        def g_thirtysecond(self):
            pass

        @property
        def no_grid(self):
            pass

    class LaunchMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def gate(self):
            pass

        @property
        def repeat(self):
            pass

        @property
        def toggle(self):
            pass

        @property
        def trigger(self):
            pass

    class MidiNote(object):
        def __init__(self, *a, *k):
            """
            An object representing a MIDI Note
            """
            pass

        @property
        def duration(self):
            pass

        @property
        def mute(self):
            pass

        @property
        def note_id(self):
            """
            A numerical ID that's unique within the originating clip of the note. Not to beused directly, but important for other API calls, namely apply_note_modifications.
            """
            pass

        @property
        def pitch(self):
            pass

        @property
        def probability(self):
            pass

        @property
        def release_velocity(self):
            pass

        @property
        def start_time(self):
            pass

        @property
        def velocity(self):
            pass

        @property
        def velocity_deviation(self):
            pass

    class MidiNoteSpecification(object):
        def __init__(self, *a, *k):
            """
            An object specifying the data for creating a MIDI note. To be used with the add_new_notes function.
            """
            pass

    class MidiNoteVector(object):
        def __init__(self, *a, *k):
            """
            A container for holding MIDI notes from Live.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<NClipApi::TNoteInfo, std::__1::allocator<NClipApi::TNoteInfo> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: MidiNoteVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<NClipApi::TNoteInfo, std::__1::allocator<NClipApi::TNoteInfo> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: MidiNoteVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

    class WarpMarker(object):
        def __init__(self, *a, *k):
            """
            This class represents a WarpMarker type.
            """
            pass

        @property
        def beat_time(self):
            """
            A WarpMarker's beat time.
            """
            pass

        @property
        def sample_time(self):
            """
            A WarpMarker's sample time.
            """
            pass

    class WarpMarkerVector(object):
        def __init__(self, *a, *k):
            """
            A container for returning warp markers from Live.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<NApiHelpers::TWarpMarker, std::__1::allocator<NApiHelpers::TWarpMarker> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: WarpMarkerVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<NApiHelpers::TWarpMarker, std::__1::allocator<NApiHelpers::TWarpMarker> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: WarpMarkerVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

    class WarpMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def beats(self):
            pass

        @property
        def complex(self):
            pass

        @property
        def complex_pro(self):
            pass

        @property
        def count(self):
            pass

        @property
        def repitch(self):
            pass

        @property
        def rex(self):
            pass

        @property
        def texture(self):
            pass

        @property
        def tones(self):
            pass


class ClipSlot(ModuleType):
    pass

    class ClipSlot(object):
        def __init__(self, *a, *k):
            """
            This class represents an entry in Lives Session view matrix.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the ClipSlot.
            """
            pass

        @property
        def clip(self):
            """
            Returns the Clip which this clipslots currently owns. Might be None.
            """
            pass

        @property
        def color(self):
            """
            Returns the canonical color for the clip slot or None if it does not exist.
            """
            pass

        @property
        def color_index(self):
            """
            Returns the canonical color index for the clip slot or None if it does not exist.
            """
            pass

        @property
        def controls_other_clips(self):
            """
            Returns true if firing this slot will fire clips in other slots.Can only be true for slots in group tracks.
            """
            pass

        @property
        def has_clip(self):
            """
            Returns true if this Clipslot owns a Clip.
            """
            pass

        @property
        def has_stop_button(self):
            """
            Get/Set if this Clip has a stop button, which will, if fired, stop anyother Clip that is currently playing the Track we do belong to.
            """
            pass

        @property
        def is_group_slot(self):
            """
            Returns whether this clip slot is a group track slot (group slot).
            """
            pass

        @property
        def is_playing(self):
            """
            Returns whether the clip associated with the slot is playing.
            """
            pass

        @property
        def is_recording(self):
            """
            Returns whether the clip associated with the slot is recording.
            """
            pass

        @property
        def is_triggered(self):
            """
            Const access to the triggering state of the clip slot.
            """
            pass

        @property
        def playing_status(self):
            """
            Const access to the playing state of the clip slot.Can be either stopped, playing, or recording.
            """
            pass

        @property
        def will_record_on_start(self):
            """
            returns true if the clip slot will record on being fired.
            """
            pass

        def add_color_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color_index" has changed. C++ signature :  void add_color_index_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_color_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color" has changed. C++ signature :  void add_color_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_controls_other_clips_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "controls_other_clips" has changed. C++ signature :  void add_controls_other_clips_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_has_clip_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "has_clip" has changed. C++ signature :  void add_has_clip_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_has_stop_button_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "has_stop_button" has changed. C++ signature :  void add_has_stop_button_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_triggered_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_triggered" has changed. C++ signature :  void add_is_triggered_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_playing_status_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "playing_status" has changed. C++ signature :  void add_playing_status_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def color_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color". C++ signature :  bool color_has_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def color_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color_index". C++ signature :  bool color_index_has_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def controls_other_clips_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "controls_other_clips". C++ signature :  bool controls_other_clips_has_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def create_clip(self, arg1, arg2):
            """
            Creates an empty clip with the given length in the slot. Throws an error when called on non-empty slots or slots in non-MIDI tracks. C++ signature :  void create_clip(TPyHandle<AGroupAndClipSlotBase>,double)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: float
            """
            pass

        def delete_clip(self, arg1):
            """
            Removes the clip contained in the slot. Raises an exception if the slot was empty. C++ signature :  void delete_clip(TPyHandle<AGroupAndClipSlotBase>)
            :param arg1: arg1
            :type arg1: ClipSlot
            """
            pass

        def duplicate_clip_to(self, arg1, arg2):
            """
            Duplicates the slot's clip to the passed in target slot. Overrides the target's clip if it's not empty. Raises an exception if the (source) slot itself is empty, or if source and target have different track types (audio vs. MIDI). Also raises if the source or target slot is in a group track (so called group slot). C++ signature :  void duplicate_clip_to(TPyHandle<AGroupAndClipSlotBase>,TPyHandle<AGroupAndClipSlotBase>)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: ClipSlot
            """
            pass

        def fire(self, arg1):
            """
            Fire a Clip if this Clipslot owns one, else trigger the stop button, if we have one. C++ signature :  void fire(TPyHandle<AGroupAndClipSlotBase>)fire( (ClipSlot)self [, (float)record_length=1.7976931348623157e+308 [, (int)launch_quantization=-2147483648 [, (bool)force_legato=False]]]) -> None : If 'record_length' is passed, the clip will be refired after the given recording length.  Raises an error if the slot owns a clip. 'launch_quantization' determines the quantization of global transport that is applied overriding the value in the song. 'force_legato' will make the clip play inmediatelly. The playhead will be moved to keep the clip synchronized. C++ signature :  void fire(TPyHandle<AGroupAndClipSlotBase> [,double=1.7976931348623157e+308 [,int=-2147483648 [,bool=False]]])
            :param arg1: arg1
            :type arg1: ClipSlot
            """
            pass

        def has_clip_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "has_clip". C++ signature :  bool has_clip_has_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def has_stop_button_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "has_stop_button". C++ signature :  bool has_stop_button_has_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_triggered_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_triggered". C++ signature :  bool is_triggered_has_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def playing_status_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "playing_status". C++ signature :  bool playing_status_has_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_color_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color_index". C++ signature :  void remove_color_index_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_color_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color". C++ signature :  void remove_color_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_controls_other_clips_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "controls_other_clips". C++ signature :  void remove_controls_other_clips_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_has_clip_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "has_clip". C++ signature :  void remove_has_clip_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_has_stop_button_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "has_stop_button". C++ signature :  void remove_has_stop_button_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_triggered_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_triggered". C++ signature :  void remove_is_triggered_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_playing_status_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "playing_status". C++ signature :  void remove_playing_status_listener(TPyHandle<AGroupAndClipSlotBase>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def set_fire_button_state(self, arg1, arg2):
            """
            Set the clipslot's fire button state directly. Supports all launch modes. C++ signature :  void set_fire_button_state(TPyHandle<AGroupAndClipSlotBase>,bool)
            :param arg1: arg1
            :type arg1: ClipSlot
            :param arg2: arg2
            :type arg2: bool
            """
            pass

        def stop(self, arg1):
            """
            Stop playing the contained Clip, if there is a Clip and its currently playing. C++ signature :  void stop(TPyHandle<AGroupAndClipSlotBase>)
            :param arg1: arg1
            :type arg1: ClipSlot
            """
            pass

    class ClipSlotPlayingState(object):
        def __init__(self, *a, *k):
            pass

        @property
        def recording(self):
            pass

        @property
        def started(self):
            pass

        @property
        def stopped(self):
            pass


class CompressorDevice(ModuleType):
    pass

    class CompressorDevice(object):
        def __init__(self, *a, *k):
            """
            This class represents a Compressor device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def available_input_routing_channels(self):
            """
            Return a list of source channels for input routing in the sidechain.
            """
            pass

        @property
        def available_input_routing_types(self):
            """
            Return a list of source types for input routing in the sidechain.
            """
            pass

        @property
        def can_have_chains(self):
            """
            Returns true if the device is a rack.
            """
            pass

        @property
        def can_have_drum_pads(self):
            """
            Returns true if the device is a drum rack.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Device.
            """
            pass

        @property
        def class_display_name(self):
            """
            Return const access to the name of the device's class name as displayed in Live's browser and device chain
            """
            pass

        @property
        def class_name(self):
            """
            Return const access to the name of the device's class.
            """
            pass

        @property
        def input_routing_channel(self):
            """
            Get and set the current source channel for input routing in the sidechain.Raises ValueError if the channel isn't one of the current values inavailable_input_routing_channels.
            """
            pass

        @property
        def input_routing_type(self):
            """
            Get and set the current source type for input routing in the sidechain.Raises ValueError if the type isn't one of the current values inavailable_input_routing_types.
            """
            pass

        @property
        def is_active(self):
            """
            Return const access to whether this device is active. This will be false bothwhen the device is off and when it's inside a rack device which is off.
            """
            pass

        @property
        def name(self):
            """
            Return access to the name of the device.
            """
            pass

        @property
        def parameters(self):
            """
            Const access to the list of available automatable parameters for this device.
            """
            pass

        @property
        def type(self):
            """
            Return the type of the device.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a device.
            """
            pass

        def add_available_input_routing_channels_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "available_input_routing_channels" has changed. C++ signature :  void add_available_input_routing_channels_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_available_input_routing_types_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "available_input_routing_types" has changed. C++ signature :  void add_available_input_routing_types_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_input_routing_channel_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "input_routing_channel" has changed. C++ signature :  void add_input_routing_channel_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_input_routing_type_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "input_routing_type" has changed. C++ signature :  void add_input_routing_type_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_active_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_active" has changed. C++ signature :  void add_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_parameters_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "parameters" has changed. C++ signature :  void add_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def available_input_routing_channels_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "available_input_routing_channels". C++ signature :  bool available_input_routing_channels_has_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def available_input_routing_types_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "available_input_routing_types". C++ signature :  bool available_input_routing_types_has_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def input_routing_channel_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "input_routing_channel". C++ signature :  bool input_routing_channel_has_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def input_routing_type_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "input_routing_type". C++ signature :  bool input_routing_type_has_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_active_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_active". C++ signature :  bool is_active_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def parameters_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "parameters". C++ signature :  bool parameters_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_available_input_routing_channels_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "available_input_routing_channels". C++ signature :  void remove_available_input_routing_channels_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_available_input_routing_types_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "available_input_routing_types". C++ signature :  void remove_available_input_routing_types_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_input_routing_channel_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "input_routing_channel". C++ signature :  void remove_input_routing_channel_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_input_routing_type_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "input_routing_type". C++ signature :  void remove_input_routing_type_listener(TCompressorDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CompressorDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_active_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_active". C++ signature :  void remove_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_parameters_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "parameters". C++ signature :  void remove_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def store_chosen_bank(self, arg1, arg2, arg3):
            """
            Set the selected bank in the device for persistency. C++ signature :  void store_chosen_bank(TPyHandle<ADevice>,int,int)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a Compressor device.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the View.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the device is shown collapsed in the device chain.
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass


class Conversions(ModuleType):
    pass

    @staticmethod
    def audio_to_midi_clip(song, audio_clip, audio_to_midi_type):
        """
        Creates a MIDI clip in a new MIDI track with the notes extracted from the given audio_clip. The `audio_to_midi_type` decides which algorithm is used in the process. Raises error when called with an inconvertible clip or invalid `audio_to_midi_type`. C++ signature :  void audio_to_midi_clip(TPyHandle<ASong>,TPyHandle<AClip>,int)
        :param song: song
        :type song: Song
        :param audio_clip: audio_clip
        :type audio_clip: Clip
        :param audio_to_midi_type: audio_to_midi_type
        :type audio_to_midi_type: int
        """
        pass

    @staticmethod
    def create_drum_rack_from_audio_clip(song, audio_clip):
        """
        Creates a new track with a drum rack with a simpler on the first pad with the specified audio clip. C++ signature :  void create_drum_rack_from_audio_clip(TPyHandle<ASong>,TPyHandle<AClip>)
        :param song: song
        :type song: Song
        :param audio_clip: audio_clip
        :type audio_clip: Clip
        """
        pass

    @staticmethod
    def create_midi_track_from_drum_pad(song, drum_pad):
        """
        Creates a new Midi track containing the specified Drum Pad's device chain. C++ signature :  void create_midi_track_from_drum_pad(TPyHandle<ASong>,TPyHandle<ADrumGroupDevicePad>)
        :param song: song
        :type song: Song
        :param drum_pad: drum_pad
        :type drum_pad: DrumPad
        """
        pass

    @staticmethod
    def create_midi_track_with_simpler(song, audio_clip):
        """
        Creates a new Midi track with a simpler including the specified audio clip. C++ signature :  void create_midi_track_with_simpler(TPyHandle<ASong>,TPyHandle<AClip>)
        :param song: song
        :type song: Song
        :param audio_clip: audio_clip
        :type audio_clip: Clip
        """
        pass

    @staticmethod
    def is_convertible_to_midi(song, audio_clip):
        """
        Returns whether `audio_clip` can be converted to MIDI. Raises error when called with a MIDI clip C++ signature :  bool is_convertible_to_midi(TPyHandle<ASong>,TPyHandle<AClip>)
        :param song: song
        :type song: Song
        :param audio_clip: audio_clip
        :type audio_clip: Clip
        :rtype: bool
        """
        pass

    @staticmethod
    def move_devices_on_track_to_new_drum_rack_pad(song, track_index):
        """
        Moves the entire device chain of the track according to the track index onto the C1 (note 36) drum pad of a new drum rack in a new track.If the track associated with the track index does not contain any devices nothing changes (i.e. a new track and new drum rack are not created). C++ signature :  TWeakPtr<TPyHandleBase> move_devices_on_track_to_new_drum_rack_pad(TPyHandle<ASong>,int)
        :param song: song
        :type song: Song
        :param track_index: track_index
        :type track_index: int
        :rtype: LomObject
        """
        pass

    @staticmethod
    def sliced_simpler_to_drum_rack(song, simpler):
        """
        Converts the Simpler into a Drum Rack, assigning each slice to a drum pad. Calling it on a non-sliced simpler raises an error. C++ signature :  void sliced_simpler_to_drum_rack(TPyHandle<ASong>,TSimplerDevicePyHandle)
        :param song: song
        :type song: Song
        :param simpler: simpler
        :type simpler: SimplerDevice
        """
        pass

    class AudioToMidiType(object):
        def __init__(self, *a, *k):
            pass

        @property
        def drums_to_midi(self):
            pass

        @property
        def harmony_to_midi(self):
            pass

        @property
        def melody_to_midi(self):
            pass


class Device(ModuleType):
    pass

    class ATimeableValueVector(object):
        def __init__(self, *a, *k):
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<TWeakPtr<ATimeableValue>, std::__1::allocator<TWeakPtr<ATimeableValue> > > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: ATimeableValueVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<TWeakPtr<ATimeableValue>, std::__1::allocator<TWeakPtr<ATimeableValue> > > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: ATimeableValueVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

    class Device(object):
        def __init__(self, *a, *k):
            """
            This class represents a MIDI or Audio DSP-Device in Live.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def can_have_chains(self):
            """
            Returns true if the device is a rack.
            """
            pass

        @property
        def can_have_drum_pads(self):
            """
            Returns true if the device is a drum rack.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Device.
            """
            pass

        @property
        def class_display_name(self):
            """
            Return const access to the name of the device's class name as displayed in Live's browser and device chain
            """
            pass

        @property
        def class_name(self):
            """
            Return const access to the name of the device's class.
            """
            pass

        @property
        def is_active(self):
            """
            Return const access to whether this device is active. This will be false bothwhen the device is off and when it's inside a rack device which is off.
            """
            pass

        @property
        def name(self):
            """
            Return access to the name of the device.
            """
            pass

        @property
        def parameters(self):
            """
            Const access to the list of available automatable parameters for this device.
            """
            pass

        @property
        def type(self):
            """
            Return the type of the device.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a device.
            """
            pass

        def add_is_active_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_active" has changed. C++ signature :  void add_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_parameters_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "parameters" has changed. C++ signature :  void add_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def is_active_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_active". C++ signature :  bool is_active_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def parameters_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "parameters". C++ signature :  bool parameters_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_is_active_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_active". C++ signature :  void remove_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_parameters_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "parameters". C++ signature :  void remove_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def store_chosen_bank(self, arg1, arg2, arg3):
            """
            Set the selected bank in the device for persistency. C++ signature :  void store_chosen_bank(TPyHandle<ADevice>,int,int)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a device.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the View.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the device is shown collapsed in the device chain.
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

    class DeviceType(object):
        def __init__(self, *a, *k):
            """
            The type of the device.
            """
            pass

        @property
        def audio_effect(self):
            """
            The type of the device.
            """
            pass

        @property
        def instrument(self):
            """
            The type of the device.
            """
            pass

        @property
        def midi_effect(self):
            """
            The type of the device.
            """
            pass

        @property
        def undefined(self):
            """
            The type of the device.
            """
            pass


class DeviceIO(ModuleType):
    pass

    class DeviceIO(object):
        def __init__(self, *a, *k):
            """
            This class represents a specific input or output bus of a device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def available_routing_channels(self):
            """
            Return a list of channels for this IO endpoint.
            """
            pass

        @property
        def available_routing_types(self):
            """
            Return a list of available routing types for this IO endpoint.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the device IO.
            """
            pass

        @property
        def default_external_routing_channel_is_none(self):
            """
            Get and set whether the default routing channel for External routing types is none.
            """
            pass

        @property
        def routing_channel(self):
            """
            Get and set the current routing channel.Raises ValueError if the channel isn't one of the current values inavailable_routing_channels.
            """
            pass

        @property
        def routing_type(self):
            """
            Get and set the current routing type.Raises ValueError if the type isn't one of the current values inavailable_routing_types.
            """
            pass

        def add_available_routing_channels_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "available_routing_channels" has changed. C++ signature :  void add_available_routing_channels_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_available_routing_types_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "available_routing_types" has changed. C++ signature :  void add_available_routing_types_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_routing_channel_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "routing_channel" has changed. C++ signature :  void add_routing_channel_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_routing_type_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "routing_type" has changed. C++ signature :  void add_routing_type_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def available_routing_channels_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "available_routing_channels". C++ signature :  bool available_routing_channels_has_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def available_routing_types_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "available_routing_types". C++ signature :  bool available_routing_types_has_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_available_routing_channels_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "available_routing_channels". C++ signature :  void remove_available_routing_channels_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_available_routing_types_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "available_routing_types". C++ signature :  void remove_available_routing_types_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_routing_channel_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "routing_channel". C++ signature :  void remove_routing_channel_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_routing_type_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "routing_type". C++ signature :  void remove_routing_type_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def routing_channel_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "routing_channel". C++ signature :  bool routing_channel_has_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def routing_type_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "routing_type". C++ signature :  bool routing_type_has_listener(TPyHandle<AMxDRoutable>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceIO
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass


class DeviceParameter(ModuleType):
    pass

    class AutomationState(object):
        def __init__(self, *a, *k):
            pass

        @property
        def none(self):
            pass

        @property
        def overridden(self):
            pass

        @property
        def playing(self):
            pass

    class DeviceParameter(object):
        def __init__(self, *a, *k):
            """
            This class represents a (automatable) parameter within a MIDI orAudio DSP-Device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def automation_state(self):
            """
            Returns state of type AutomationState.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the device parameter.
            """
            pass

        @property
        def default_value(self):
            """
            Return the default value for this parameter.  A Default value is onlyavailable for non-quantized parameter types (see 'is_quantized').
            """
            pass

        @property
        def is_enabled(self):
            """
            Returns false if the parameter has been macro mapped or disabled by Max.
            """
            pass

        @property
        def is_quantized(self):
            """
            Returns True, if this value is a boolean or integer like switch.Non quantized values are continues float values.
            """
            pass

        @property
        def max(self):
            """
            Returns const access to the upper value of the allowed range forthis parameter
            """
            pass

        @property
        def min(self):
            """
            Returns const access to the lower value of the allowed range forthis parameter
            """
            pass

        @property
        def name(self):
            """
            Returns const access the name of this parameter, as visible in Livesautomation choosers.
            """
            pass

        @property
        def original_name(self):
            """
            Returns const access the original name of this parameter, unaffected ofany renamings.
            """
            pass

        @property
        def state(self):
            """
            Returns the state of the parameter:- enabled - the parameter's value can be changed,- irrelevant - the parameter is enabled, but value changes will not take any effect until it gets enabled,- disabled - the parameter's value cannot be changed.
            """
            pass

        @property
        def value(self):
            """
            Get/Set the current value (as visible in the GUI) this parameter.The value must be inside the min/max properties of this device.
            """
            pass

        @property
        def value_items(self):
            """
            Return the list of possible values for this parameter. Raises an error if 'is_quantized' is False.
            """
            pass

        def add_automation_state_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "automation_state" has changed. C++ signature :  void add_automation_state_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_state_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "state" has changed. C++ signature :  void add_state_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_value_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "value" has changed. C++ signature :  void add_value_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def automation_state_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "automation_state". C++ signature :  bool automation_state_has_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def begin_gesture(self, arg1):
            """
            Notify the begin of a modification of the parameter, when a sequence of modifications have to be consider a consistent group -- for Sexample, when recording automation. C++ signature :  void begin_gesture(TPyHandle<ATimeableValue>)
            :param arg1: arg1
            :type arg1: DeviceParameter
            """
            pass

        def end_gesture(self, arg1):
            """
            Notify the end of a modification of the parameter. See begin_gesture. C++ signature :  void end_gesture(TPyHandle<ATimeableValue>)
            :param arg1: arg1
            :type arg1: DeviceParameter
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def re_enable_automation(self, arg1):
            """
            Reenable automation for this parameter. C++ signature :  void re_enable_automation(TPyHandle<ATimeableValue>)
            :param arg1: arg1
            :type arg1: DeviceParameter
            """
            pass

        def remove_automation_state_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "automation_state". C++ signature :  void remove_automation_state_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_state_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "state". C++ signature :  void remove_state_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_value_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "value". C++ signature :  void remove_value_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def state_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "state". C++ signature :  bool state_has_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def str_for_value(self, arg1, arg2):
            """
            Return a string representation of the given value. To be used for display purposes only.  This value can include characters like 'db' or 'hz', depending on the type of the parameter. C++ signature :  TString str_for_value(TPyHandle<ATimeableValue>,float)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: float
            :rtype: unicode
            """
            pass

        def value_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "value". C++ signature :  bool value_has_listener(TPyHandle<ATimeableValue>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DeviceParameter
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

    class ParameterState(object):
        def __init__(self, *a, *k):
            pass

        @property
        def disabled(self):
            pass

        @property
        def enabled(self):
            pass

        @property
        def irrelevant(self):
            pass


class DrumChain(ModuleType):
    pass

    class DrumChain(object):
        def __init__(self, *a, *k):
            """
            This class represents a drum group device chain in Live.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the chain.
            """
            pass

        @property
        def choke_group(self):
            """
            Access to the chain's choke group setting.
            """
            pass

        @property
        def color(self):
            """
            Access the color index of the Chain.
            """
            pass

        @property
        def color_index(self):
            """
            Access the color index of the Chain.
            """
            pass

        @property
        def devices(self):
            """
            Return const access to all available Devices that are present in the chains
            """
            pass

        @property
        def has_audio_input(self):
            """
            return True, if this Chain can be feed with an Audio signal. This istrue for all Audio Chains.
            """
            pass

        @property
        def has_audio_output(self):
            """
            return True, if this Chain sends out an Audio signal. This istrue for all Audio Chains, and MIDI chains with an Instrument.
            """
            pass

        @property
        def has_midi_input(self):
            """
            return True, if this Chain can be feed with an Audio signal. This istrue for all MIDI Chains.
            """
            pass

        @property
        def has_midi_output(self):
            """
            return True, if this Chain sends out MIDI events. This istrue for all MIDI Chains with no Instruments.
            """
            pass

        @property
        def is_auto_colored(self):
            """
            Get/set access to the auto color flag of the Chain.If True, the Chain will always have the same color as the containingTrack or Chain.
            """
            pass

        @property
        def mixer_device(self):
            """
            Return access to the mixer device that holds the chain's mixer parameters:the Volume, Pan, and Sendamounts.
            """
            pass

        @property
        def mute(self):
            """
            Mute/unmute the chain.
            """
            pass

        @property
        def muted_via_solo(self):
            """
            Return const access to whether this chain is muted due to some other chainbeing soloed.
            """
            pass

        @property
        def name(self):
            """
            Read/write access to the name of the Chain, as visible in the track header.
            """
            pass

        @property
        def out_note(self):
            """
            Access to the MIDI note sent to the devices in the chain.
            """
            pass

        @property
        def solo(self):
            """
            Get/Set the solo status of the chain. Note that this will not disable thesolo state of any other Chain in the same rack. If you want exclusive solo, you have to disable the solo state of the other Chains manually.
            """
            pass

        def add_choke_group_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "choke_group" has changed. C++ signature :  void add_choke_group_listener(TDrumChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumChain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_color_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color_index" has changed. C++ signature :  void add_color_index_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_color_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color" has changed. C++ signature :  void add_color_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_devices_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "devices" has changed. C++ signature :  void add_devices_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_auto_colored_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_auto_colored" has changed. C++ signature :  void add_is_auto_colored_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_mute_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "mute" has changed. C++ signature :  void add_mute_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_muted_via_solo_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "muted_via_solo" has changed. C++ signature :  void add_muted_via_solo_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_out_note_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "out_note" has changed. C++ signature :  void add_out_note_listener(TDrumChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumChain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_solo_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "solo" has changed. C++ signature :  void add_solo_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def choke_group_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "choke_group". C++ signature :  bool choke_group_has_listener(TDrumChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumChain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def color_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color". C++ signature :  bool color_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def color_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color_index". C++ signature :  bool color_index_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def delete_device(self, arg1, arg2):
            """
            Remove a device identified by its index from the chain. Throws runtime error if bad index.  C++ signature :  void delete_device(TChainPyHandle,int)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: int
            """
            pass

        def devices_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "devices". C++ signature :  bool devices_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_auto_colored_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_auto_colored". C++ signature :  bool is_auto_colored_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def mute_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "mute". C++ signature :  bool mute_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def muted_via_solo_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "muted_via_solo". C++ signature :  bool muted_via_solo_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def out_note_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "out_note". C++ signature :  bool out_note_has_listener(TDrumChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumChain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_choke_group_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "choke_group". C++ signature :  void remove_choke_group_listener(TDrumChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumChain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_color_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color_index". C++ signature :  void remove_color_index_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_color_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color". C++ signature :  void remove_color_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_devices_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "devices". C++ signature :  void remove_devices_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_auto_colored_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_auto_colored". C++ signature :  void remove_is_auto_colored_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_mute_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "mute". C++ signature :  void remove_mute_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_muted_via_solo_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "muted_via_solo". C++ signature :  void remove_muted_via_solo_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_out_note_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "out_note". C++ signature :  void remove_out_note_listener(TDrumChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumChain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_solo_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "solo". C++ signature :  void remove_solo_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def solo_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "solo". C++ signature :  bool solo_has_listener(TChainPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Chain
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass


class DrumPad(ModuleType):
    pass

    class DrumPad(object):
        def __init__(self, *a, *k):
            """
            This class represents a drum group device pad in Live.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the drum pad.
            """
            pass

        @property
        def chains(self):
            """
            Return const access to the list of chains in this drum pad.
            """
            pass

        @property
        def mute(self):
            """
            Mute/unmute the pad.
            """
            pass

        @property
        def name(self):
            """
            Return const access to the drum pad's name. It depends on the contained chains.
            """
            pass

        @property
        def note(self):
            """
            Get the MIDI note of the drum pad.
            """
            pass

        @property
        def solo(self):
            """
            Solo/unsolo the pad.
            """
            pass

        def add_chains_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "chains" has changed. C++ signature :  void add_chains_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_mute_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "mute" has changed. C++ signature :  void add_mute_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_solo_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "solo" has changed. C++ signature :  void add_solo_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def chains_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "chains". C++ signature :  bool chains_has_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def delete_all_chains(self, arg1):
            """
            Deletes all chains associated with a drum pad. This is equivalent to deleting a drum rack pad in Live. C++ signature :  void delete_all_chains(TPyHandle<ADrumGroupDevicePad>)
            :param arg1: arg1
            :type arg1: DrumPad
            """
            pass

        def mute_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "mute". C++ signature :  bool mute_has_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_chains_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "chains". C++ signature :  void remove_chains_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_mute_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "mute". C++ signature :  void remove_mute_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_solo_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "solo". C++ signature :  void remove_solo_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def solo_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "solo". C++ signature :  bool solo_has_listener(TPyHandle<ADrumGroupDevicePad>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: DrumPad
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass


class Eq8Device(ModuleType):
    pass

    class EditMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def a(self):
            pass

        @property
        def b(self):
            pass

    class Eq8Device(object):
        def __init__(self, *a, *k):
            """
            This class represents an Eq8 device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def can_have_chains(self):
            """
            Returns true if the device is a rack.
            """
            pass

        @property
        def can_have_drum_pads(self):
            """
            Returns true if the device is a drum rack.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Device.
            """
            pass

        @property
        def class_display_name(self):
            """
            Return const access to the name of the device's class name as displayed in Live's browser and device chain
            """
            pass

        @property
        def class_name(self):
            """
            Return const access to the name of the device's class.
            """
            pass

        @property
        def edit_mode(self):
            """
            Access to Eq8's edit mode.
            """
            pass

        @property
        def global_mode(self):
            """
            Access to Eq8's global mode.
            """
            pass

        @property
        def is_active(self):
            """
            Return const access to whether this device is active. This will be false bothwhen the device is off and when it's inside a rack device which is off.
            """
            pass

        @property
        def name(self):
            """
            Return access to the name of the device.
            """
            pass

        @property
        def oversample(self):
            """
            Access to Eq8's oversample value.
            """
            pass

        @property
        def parameters(self):
            """
            Const access to the list of available automatable parameters for this device.
            """
            pass

        @property
        def type(self):
            """
            Return the type of the device.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a device.
            """
            pass

        def add_edit_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "edit_mode" has changed. C++ signature :  void add_edit_mode_listener(TEq8DevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Eq8Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_global_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "global_mode" has changed. C++ signature :  void add_global_mode_listener(TEq8DevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Eq8Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_active_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_active" has changed. C++ signature :  void add_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_oversample_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "oversample" has changed. C++ signature :  void add_oversample_listener(TEq8DevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Eq8Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_parameters_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "parameters" has changed. C++ signature :  void add_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def edit_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "edit_mode". C++ signature :  bool edit_mode_has_listener(TEq8DevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Eq8Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def global_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "global_mode". C++ signature :  bool global_mode_has_listener(TEq8DevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Eq8Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_active_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_active". C++ signature :  bool is_active_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def oversample_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "oversample". C++ signature :  bool oversample_has_listener(TEq8DevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Eq8Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def parameters_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "parameters". C++ signature :  bool parameters_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_edit_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "edit_mode". C++ signature :  void remove_edit_mode_listener(TEq8DevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Eq8Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_global_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "global_mode". C++ signature :  void remove_global_mode_listener(TEq8DevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Eq8Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_active_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_active". C++ signature :  void remove_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_oversample_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "oversample". C++ signature :  void remove_oversample_listener(TEq8DevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Eq8Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_parameters_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "parameters". C++ signature :  void remove_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def store_chosen_bank(self, arg1, arg2, arg3):
            """
            Set the selected bank in the device for persistency. C++ signature :  void store_chosen_bank(TPyHandle<ADevice>,int,int)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of an Eq8 device.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the View.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the device is shown collapsed in the device chain.
                """
                pass

            @property
            def selected_band(self):
                """
                Access to the selected filter band.
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_selected_band_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "selected_band" has changed. C++ signature :  void add_selected_band_listener(TEq8DevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_selected_band_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "selected_band". C++ signature :  void remove_selected_band_listener(TEq8DevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def selected_band_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "selected_band". C++ signature :  bool selected_band_has_listener(TEq8DevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

    class GlobalMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def left_right(self):
            pass

        @property
        def mid_side(self):
            pass

        @property
        def stereo(self):
            pass


class Groove(ModuleType):
    pass

    class Base(object):
        def __init__(self, *a, *k):
            pass

        @property
        def count(self):
            pass

        @property
        def gb_eight(self):
            pass

        @property
        def gb_eight_triplet(self):
            pass

        @property
        def gb_four(self):
            pass

        @property
        def gb_sixteen(self):
            pass

        @property
        def gb_sixteen_triplet(self):
            pass

        @property
        def gb_thirtytwo(self):
            pass

    class Groove(object):
        def __init__(self, *a, *k):
            """
            This class represents a groove in Live.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def base(self):
            """
            Get/set the groove's base grid.
            """
            pass

        @property
        def name(self):
            """
            Read/write/listen access to the groove's name
            """
            pass

        @property
        def quantization_amount(self):
            """
            Read/write/listen access to the groove's quantization amount.
            """
            pass

        @property
        def random_amount(self):
            """
            Read/write/listen access to the groove's random amount.
            """
            pass

        @property
        def timing_amount(self):
            """
            Read/write/listen access to the groove's timing amount.
            """
            pass

        @property
        def velocity_amount(self):
            """
            Read/write/listen access to the groove's velocity amount.
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_quantization_amount_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "quantization_amount" has changed. C++ signature :  void add_quantization_amount_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_random_amount_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "random_amount" has changed. C++ signature :  void add_random_amount_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_timing_amount_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "timing_amount" has changed. C++ signature :  void add_timing_amount_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_velocity_amount_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "velocity_amount" has changed. C++ signature :  void add_velocity_amount_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def quantization_amount_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "quantization_amount". C++ signature :  bool quantization_amount_has_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def random_amount_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "random_amount". C++ signature :  bool random_amount_has_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_quantization_amount_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "quantization_amount". C++ signature :  void remove_quantization_amount_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_random_amount_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "random_amount". C++ signature :  void remove_random_amount_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_timing_amount_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "timing_amount". C++ signature :  void remove_timing_amount_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_velocity_amount_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "velocity_amount". C++ signature :  void remove_velocity_amount_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def timing_amount_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "timing_amount". C++ signature :  bool timing_amount_has_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def velocity_amount_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "velocity_amount". C++ signature :  bool velocity_amount_has_listener(TPyHandle<AGroove>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Groove
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass


class GroovePool(ModuleType):
    pass

    class GroovePool(object):
        def __init__(self, *a, *k):
            """
            This class represents the groove pool in Live.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def grooves(self):
            """
            Access to the list of grooves
            """
            pass

        def add_grooves_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "grooves" has changed. C++ signature :  void add_grooves_listener(TPyHandle<AGroovePool>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: GroovePool
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def grooves_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "grooves". C++ signature :  bool grooves_has_listener(TPyHandle<AGroovePool>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: GroovePool
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_grooves_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "grooves". C++ signature :  void remove_grooves_listener(TPyHandle<AGroovePool>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: GroovePool
            :param arg2: arg2
            :type arg2: object
            """
            pass


class HybridReverbDevice(ModuleType):
    pass

    class HybridReverbDevice(object):
        def __init__(self, *a, *k):
            """
            This class represents a Hybrid Reverb device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def can_have_chains(self):
            """
            Returns true if the device is a rack.
            """
            pass

        @property
        def can_have_drum_pads(self):
            """
            Returns true if the device is a drum rack.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Device.
            """
            pass

        @property
        def class_display_name(self):
            """
            Return const access to the name of the device's class name as displayed in Live's browser and device chain
            """
            pass

        @property
        def class_name(self):
            """
            Return const access to the name of the device's class.
            """
            pass

        @property
        def ir_attack_time(self):
            """
            Return the current IrAttackTime
            """
            pass

        @property
        def ir_category_index(self):
            """
            Return the current IR category index
            """
            pass

        @property
        def ir_category_list(self):
            """
            Return the current IR categories list
            """
            pass

        @property
        def ir_decay_time(self):
            """
            Return the current IrDecayTime
            """
            pass

        @property
        def ir_file_index(self):
            """
            Return the current IR file index
            """
            pass

        @property
        def ir_file_list(self):
            """
            Return the current IR file list
            """
            pass

        @property
        def ir_size_factor(self):
            """
            Return the current IrSizeFactor
            """
            pass

        @property
        def ir_time_shaping_on(self):
            """
            Return the current IrTimeShapingOn
            """
            pass

        @property
        def is_active(self):
            """
            Return const access to whether this device is active. This will be false bothwhen the device is off and when it's inside a rack device which is off.
            """
            pass

        @property
        def name(self):
            """
            Return access to the name of the device.
            """
            pass

        @property
        def parameters(self):
            """
            Const access to the list of available automatable parameters for this device.
            """
            pass

        @property
        def type(self):
            """
            Return the type of the device.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a device.
            """
            pass

        def add_ir_attack_time_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "ir_attack_time" has changed. C++ signature :  void add_ir_attack_time_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_ir_category_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "ir_category_index" has changed. C++ signature :  void add_ir_category_index_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_ir_decay_time_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "ir_decay_time" has changed. C++ signature :  void add_ir_decay_time_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_ir_file_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "ir_file_index" has changed. C++ signature :  void add_ir_file_index_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_ir_file_list_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "ir_file_list" has changed. C++ signature :  void add_ir_file_list_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_ir_size_factor_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "ir_size_factor" has changed. C++ signature :  void add_ir_size_factor_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_ir_time_shaping_on_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "ir_time_shaping_on" has changed. C++ signature :  void add_ir_time_shaping_on_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_active_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_active" has changed. C++ signature :  void add_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_parameters_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "parameters" has changed. C++ signature :  void add_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def ir_attack_time_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "ir_attack_time". C++ signature :  bool ir_attack_time_has_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def ir_category_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "ir_category_index". C++ signature :  bool ir_category_index_has_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def ir_decay_time_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "ir_decay_time". C++ signature :  bool ir_decay_time_has_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def ir_file_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "ir_file_index". C++ signature :  bool ir_file_index_has_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def ir_file_list_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "ir_file_list". C++ signature :  bool ir_file_list_has_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def ir_size_factor_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "ir_size_factor". C++ signature :  bool ir_size_factor_has_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def ir_time_shaping_on_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "ir_time_shaping_on". C++ signature :  bool ir_time_shaping_on_has_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_active_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_active". C++ signature :  bool is_active_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def parameters_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "parameters". C++ signature :  bool parameters_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_ir_attack_time_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "ir_attack_time". C++ signature :  void remove_ir_attack_time_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_ir_category_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "ir_category_index". C++ signature :  void remove_ir_category_index_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_ir_decay_time_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "ir_decay_time". C++ signature :  void remove_ir_decay_time_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_ir_file_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "ir_file_index". C++ signature :  void remove_ir_file_index_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_ir_file_list_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "ir_file_list". C++ signature :  void remove_ir_file_list_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_ir_size_factor_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "ir_size_factor". C++ signature :  void remove_ir_size_factor_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_ir_time_shaping_on_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "ir_time_shaping_on". C++ signature :  void remove_ir_time_shaping_on_listener(THybridReverbDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: HybridReverbDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_active_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_active". C++ signature :  void remove_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_parameters_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "parameters". C++ signature :  void remove_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def store_chosen_bank(self, arg1, arg2, arg3):
            """
            Set the selected bank in the device for persistency. C++ signature :  void store_chosen_bank(TPyHandle<ADevice>,int,int)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a device.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the View.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the device is shown collapsed in the device chain.
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass


class Listener(ModuleType):
    pass

    class ListenerHandle(object):
        def __init__(self, *a, *k):
            """
            This class represents a Python listener when connected to a Live property.
            """
            pass

        @property
        def listener_func(self):
            """
            Returns the original function
            """
            pass

        @property
        def listener_self(self):
            """
            Returns the weak reference to original self, if it was a bound method
            """
            pass

        @property
        def name(self):
            """
            Prints the name of the property that this listener is connected to
            """
            pass

        def disconnect(self, arg1):
            """
            Disconnects the listener from its property C++ signature :  void disconnect(LPythonRemote {lvalue})
            :param arg1: arg1
            :type arg1: ListenerHandle
            """
            pass

    class ListenerVector(object):
        def __init__(self, *a, *k):
            """
            A read only container for accessing a list of listeners.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<TWeakPtr<LPythonRemote>, std::__1::allocator<TWeakPtr<LPythonRemote> > > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: ListenerVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<TWeakPtr<LPythonRemote>, std::__1::allocator<TWeakPtr<LPythonRemote> > > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: ListenerVector
            :param arg2: arg2
            :type arg2: object
            """
            pass


class LomObject(ModuleType):
    pass

    class LomObject(object):
        def __init__(self, *a, *k):
            """
            this is the base class for an object that is accessible via the LOM
            """
            pass

        @property
        def _live_ptr(self):
            pass


class MaxDevice(ModuleType):
    pass

    class MaxDevice(object):
        def __init__(self, *a, *k):
            """
            This class represents a Max for Live device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def audio_inputs(self):
            """
            Const access to a list of all audio inputs of the device.
            """
            pass

        @property
        def audio_outputs(self):
            """
            Const access to a list of all audio outputs of the device.
            """
            pass

        @property
        def can_have_chains(self):
            """
            Returns true if the device is a rack.
            """
            pass

        @property
        def can_have_drum_pads(self):
            """
            Returns true if the device is a drum rack.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Device.
            """
            pass

        @property
        def class_display_name(self):
            """
            Return const access to the name of the device's class name as displayed in Live's browser and device chain
            """
            pass

        @property
        def class_name(self):
            """
            Return const access to the name of the device's class.
            """
            pass

        @property
        def is_active(self):
            """
            Return const access to whether this device is active. This will be false bothwhen the device is off and when it's inside a rack device which is off.
            """
            pass

        @property
        def midi_inputs(self):
            """
            Const access to a list of all midi outputs of the device.
            """
            pass

        @property
        def midi_outputs(self):
            """
            Const access to a list of all midi outputs of the device.
            """
            pass

        @property
        def name(self):
            """
            Return access to the name of the device.
            """
            pass

        @property
        def parameters(self):
            """
            Const access to the list of available automatable parameters for this device.
            """
            pass

        @property
        def type(self):
            """
            Return the type of the device.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a device.
            """
            pass

        def add_audio_inputs_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "audio_inputs" has changed. C++ signature :  void add_audio_inputs_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_audio_outputs_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "audio_outputs" has changed. C++ signature :  void add_audio_outputs_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_bank_parameters_changed_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "bank_parameters_changed" has changed. C++ signature :  void add_bank_parameters_changed_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_active_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_active" has changed. C++ signature :  void add_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_midi_inputs_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "midi_inputs" has changed. C++ signature :  void add_midi_inputs_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_midi_outputs_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "midi_outputs" has changed. C++ signature :  void add_midi_outputs_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_parameters_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "parameters" has changed. C++ signature :  void add_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def audio_inputs_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "audio_inputs". C++ signature :  bool audio_inputs_has_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def audio_outputs_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "audio_outputs". C++ signature :  bool audio_outputs_has_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def bank_parameters_changed_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "bank_parameters_changed". C++ signature :  bool bank_parameters_changed_has_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def get_bank_count(self, arg1):
            """
            Get the number of parameter banks. This is related to hardware control surfaces. C++ signature :  int get_bank_count(TMaxDevicePyHandle)
            :param arg1: arg1
            :type arg1: MaxDevice
            :rtype: int
            """
            pass

        def get_bank_name(self, arg1, arg2):
            """
            Get the name of a parameter bank given by index. This is related to hardware control surfaces. C++ signature :  TString get_bank_name(TMaxDevicePyHandle,int)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: int
            :rtype: unicode
            """
            pass

        def get_bank_parameters(self, arg1, arg2):
            """
            Get the indices of parameters of the given bank index. Empty slots are marked as -1. Bank index -1 refers to the best-of bank. This function is related to hardware control surfaces. C++ signature :  boost::python::list get_bank_parameters(TMaxDevicePyHandle,int)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: int
            :rtype: list
            """
            pass

        def get_value_item_icons(self, arg1, arg2):
            """
            Get a list of icon identifier strings for a list parameter's values.An empty string is given where no icon should be displayed.An empty list is given when no icons should be displayed.This is related to hardware control surfaces. C++ signature :  boost::python::list get_value_item_icons(TMaxDevicePyHandle,TPyHandle<ATimeableValue>)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: DeviceParameter
            :rtype: list
            """
            pass

        def is_active_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_active". C++ signature :  bool is_active_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def midi_inputs_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "midi_inputs". C++ signature :  bool midi_inputs_has_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def midi_outputs_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "midi_outputs". C++ signature :  bool midi_outputs_has_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def parameters_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "parameters". C++ signature :  bool parameters_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_audio_inputs_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "audio_inputs". C++ signature :  void remove_audio_inputs_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_audio_outputs_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "audio_outputs". C++ signature :  void remove_audio_outputs_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_bank_parameters_changed_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "bank_parameters_changed". C++ signature :  void remove_bank_parameters_changed_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_active_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_active". C++ signature :  void remove_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_midi_inputs_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "midi_inputs". C++ signature :  void remove_midi_inputs_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_midi_outputs_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "midi_outputs". C++ signature :  void remove_midi_outputs_listener(TMaxDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MaxDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_parameters_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "parameters". C++ signature :  void remove_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def store_chosen_bank(self, arg1, arg2, arg3):
            """
            Set the selected bank in the device for persistency. C++ signature :  void store_chosen_bank(TPyHandle<ADevice>,int,int)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a device.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the View.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the device is shown collapsed in the device chain.
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass


class MidiMap(ModuleType):
    pass

    @staticmethod
    def forward_midi_cc(arg1, arg2, arg3, arg4, ShouldConsumeEvent=True):
        """
        C++ signature :  bool forward_midi_cc(unsigned int,unsigned int,int,int [,bool=True])
        :param arg1: arg1
        :type arg1: int
        :param arg2: arg2
        :type arg2: int
        :param arg3: arg3
        :type arg3: int
        :param arg4: arg4
        :type arg4: int
        :param ShouldConsumeEvent: ShouldConsumeEvent defaults to True 
        :type ShouldConsumeEvent: bool
        :rtype: bool
        """
        pass

    @staticmethod
    def forward_midi_note(arg1, arg2, arg3, arg4, ShouldConsumeEvent=True):
        """
        C++ signature :  bool forward_midi_note(unsigned int,unsigned int,int,int [,bool=True])
        :param arg1: arg1
        :type arg1: int
        :param arg2: arg2
        :type arg2: int
        :param arg3: arg3
        :type arg3: int
        :param arg4: arg4
        :type arg4: int
        :param ShouldConsumeEvent: ShouldConsumeEvent defaults to True 
        :type ShouldConsumeEvent: bool
        :rtype: bool
        """
        pass

    @staticmethod
    def forward_midi_pitchbend(arg1, arg2, arg3):
        """
        C++ signature :  bool forward_midi_pitchbend(unsigned int,unsigned int,int)
        :param arg1: arg1
        :type arg1: int
        :param arg2: arg2
        :type arg2: int
        :param arg3: arg3
        :type arg3: int
        :rtype: bool
        """
        pass

    @staticmethod
    def map_midi_cc(midi_map_handle, parameter, midi_channel, controller_number, map_mode, avoid_takeover, sensitivity=1.0):
        """
        C++ signature :  bool map_midi_cc(unsigned int,TPyHandle<ATimeableValue>,int,int,NRemoteMapperTypes::TControllerMapMode,bool [,float=1.0])
        :param midi_map_handle: midi_map_handle
        :type midi_map_handle: int
        :param parameter: parameter
        :type parameter: DeviceParameter
        :param midi_channel: midi_channel
        :type midi_channel: int
        :param controller_number: controller_number
        :type controller_number: int
        :param map_mode: map_mode
        :type map_mode: MapMode
        :param avoid_takeover: avoid_takeover
        :type avoid_takeover: bool
        :param sensitivity: sensitivity defaults to 1.0 
        :type sensitivity: float
        :rtype: bool
        """
        pass

    @staticmethod
    def map_midi_cc_with_feedback_map(midi_map_handle, parameter, midi_channel, controller_number, map_mode, feedback_rule, avoid_takeover, sensitivity=1.0):
        """
        C++ signature :  bool map_midi_cc_with_feedback_map(unsigned int,TPyHandle<ATimeableValue>,int,int,NRemoteMapperTypes::TControllerMapMode,NPythonMidiMap::TCCFeedbackRule,bool [,float=1.0])
        :param midi_map_handle: midi_map_handle
        :type midi_map_handle: int
        :param parameter: parameter
        :type parameter: DeviceParameter
        :param midi_channel: midi_channel
        :type midi_channel: int
        :param controller_number: controller_number
        :type controller_number: int
        :param map_mode: map_mode
        :type map_mode: MapMode
        :param feedback_rule: feedback_rule
        :type feedback_rule: CCFeedbackRule
        :param avoid_takeover: avoid_takeover
        :type avoid_takeover: bool
        :param sensitivity: sensitivity defaults to 1.0 
        :type sensitivity: float
        :rtype: bool
        """
        pass

    @staticmethod
    def map_midi_note(arg1, arg2, arg3, arg4):
        """
        C++ signature :  bool map_midi_note(unsigned int,TPyHandle<ATimeableValue>,int,int)
        :param arg1: arg1
        :type arg1: int
        :param arg2: arg2
        :type arg2: DeviceParameter
        :param arg3: arg3
        :type arg3: int
        :param arg4: arg4
        :type arg4: int
        :rtype: bool
        """
        pass

    @staticmethod
    def map_midi_note_with_feedback_map(arg1, arg2, arg3, arg4, arg5):
        """
        C++ signature :  bool map_midi_note_with_feedback_map(unsigned int,TPyHandle<ATimeableValue>,int,int,NPythonMidiMap::TNoteFeedbackRule)
        :param arg1: arg1
        :type arg1: int
        :param arg2: arg2
        :type arg2: DeviceParameter
        :param arg3: arg3
        :type arg3: int
        :param arg4: arg4
        :type arg4: int
        :param arg5: arg5
        :type arg5: NoteFeedbackRule
        :rtype: bool
        """
        pass

    @staticmethod
    def map_midi_pitchbend(arg1, arg2, arg3, arg4):
        """
        C++ signature :  bool map_midi_pitchbend(unsigned int,TPyHandle<ATimeableValue>,int,bool)
        :param arg1: arg1
        :type arg1: int
        :param arg2: arg2
        :type arg2: DeviceParameter
        :param arg3: arg3
        :type arg3: int
        :param arg4: arg4
        :type arg4: bool
        :rtype: bool
        """
        pass

    @staticmethod
    def map_midi_pitchbend_with_feedback_map(arg1, arg2, arg3, arg4, arg5):
        """
        C++ signature :  bool map_midi_pitchbend_with_feedback_map(unsigned int,TPyHandle<ATimeableValue>,int,NPythonMidiMap::TPitchBendFeedbackRule,bool)
        :param arg1: arg1
        :type arg1: int
        :param arg2: arg2
        :type arg2: DeviceParameter
        :param arg3: arg3
        :type arg3: int
        :param arg4: arg4
        :type arg4: PitchBendFeedbackRule
        :param arg5: arg5
        :type arg5: bool
        :rtype: bool
        """
        pass

    @staticmethod
    def send_feedback_for_parameter(arg1, arg2):
        """
        C++ signature :  void send_feedback_for_parameter(unsigned int,TPyHandle<ATimeableValue>)
        :param arg1: arg1
        :type arg1: int
        :param arg2: arg2
        :type arg2: DeviceParameter
        """
        pass

    class CCFeedbackRule(object):
        def __init__(self, *a, *k):
            """
            Structure to define feedback properties of MIDI mappings.
            """
            pass

        @property
        def cc_no(self):
            pass

        @property
        def cc_value_map(self):
            pass

        @property
        def channel(self):
            pass

        @property
        def delay_in_ms(self):
            pass

    class MapMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def absolute(self):
            pass

        @property
        def absolute_14_bit(self):
            pass

        @property
        def relative_binary_offset(self):
            pass

        @property
        def relative_signed_bit(self):
            pass

        @property
        def relative_signed_bit2(self):
            pass

        @property
        def relative_smooth_binary_offset(self):
            pass

        @property
        def relative_smooth_signed_bit(self):
            pass

        @property
        def relative_smooth_signed_bit2(self):
            pass

        @property
        def relative_smooth_two_compliment(self):
            pass

        @property
        def relative_two_compliment(self):
            pass

    class NoteFeedbackRule(object):
        def __init__(self, *a, *k):
            """
            Structure to define feedback properties of MIDI mappings.
            """
            pass

        @property
        def channel(self):
            pass

        @property
        def delay_in_ms(self):
            pass

        @property
        def note_no(self):
            pass

        @property
        def vel_map(self):
            pass

    class PitchBendFeedbackRule(object):
        def __init__(self, *a, *k):
            """
            Structure to define feedback properties of MIDI mappings.
            """
            pass

        @property
        def channel(self):
            pass

        @property
        def delay_in_ms(self):
            pass

        @property
        def value_pair_map(self):
            pass


class MixerDevice(ModuleType):
    pass

    class MixerDevice(object):
        def __init__(self, *a, *k):
            """
            This class represents a Mixer Device in Live, which gives youaccess to the Volume and Panning properties of a Track.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the mixer device.
            """
            pass

        @property
        def crossfade_assign(self):
            """
            Player- and ReturnTracks only: Access to the Track's Crossfade Assign State.
            """
            pass

        @property
        def crossfader(self):
            """
            MasterTrack only: Const access to the Crossfader.
            """
            pass

        @property
        def cue_volume(self):
            """
            MasterTrack only: Const access to the Cue Volume Parameter.
            """
            pass

        @property
        def left_split_stereo(self):
            """
            Const access to the Track's Left Split Stereo Panning Device Parameter.
            """
            pass

        @property
        def panning(self):
            """
            Const access to the Tracks Panning Device Parameter.
            """
            pass

        @property
        def panning_mode(self):
            """
            Access to the Track's Panning Mode.
            """
            pass

        @property
        def right_split_stereo(self):
            """
            Const access to the Track's Right Split Stereo Panning Device Parameter.
            """
            pass

        @property
        def sends(self):
            """
            Const access to the Tracks list of Send Amount Device Parameters.
            """
            pass

        @property
        def song_tempo(self):
            """
            MasterTrack only: Const access to the Song's Tempo.
            """
            pass

        @property
        def track_activator(self):
            """
            Const access to the Tracks Activator Device Parameter.
            """
            pass

        @property
        def volume(self):
            """
            Const access to the Tracks Volume Device Parameter.
            """
            pass

        def add_crossfade_assign_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "crossfade_assign" has changed. C++ signature :  void add_crossfade_assign_listener(TPyHandle<ATrackDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MixerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_panning_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "panning_mode" has changed. C++ signature :  void add_panning_mode_listener(TPyHandle<ATrackDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MixerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_sends_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "sends" has changed. C++ signature :  void add_sends_listener(TPyHandle<ATrackDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MixerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def crossfade_assign_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "crossfade_assign". C++ signature :  bool crossfade_assign_has_listener(TPyHandle<ATrackDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MixerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def panning_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "panning_mode". C++ signature :  bool panning_mode_has_listener(TPyHandle<ATrackDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MixerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_crossfade_assign_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "crossfade_assign". C++ signature :  void remove_crossfade_assign_listener(TPyHandle<ATrackDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MixerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_panning_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "panning_mode". C++ signature :  void remove_panning_mode_listener(TPyHandle<ATrackDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MixerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_sends_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "sends". C++ signature :  void remove_sends_listener(TPyHandle<ATrackDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MixerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def sends_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "sends". C++ signature :  bool sends_has_listener(TPyHandle<ATrackDevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: MixerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        class crossfade_assignments(object):
            def __init__(self, *a, *k):
                pass

            @property
            def A(self):
                pass

            @property
            def B(self):
                pass

            @property
            def NONE(self):
                pass

        class panning_modes(object):
            def __init__(self, *a, *k):
                pass

            @property
            def stereo(self):
                pass

            @property
            def stereo_split(self):
                pass


class PluginDevice(ModuleType):
    pass

    class PluginDevice(object):
        def __init__(self, *a, *k):
            """
            This class represents a plugin device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def can_have_chains(self):
            """
            Returns true if the device is a rack.
            """
            pass

        @property
        def can_have_drum_pads(self):
            """
            Returns true if the device is a drum rack.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Device.
            """
            pass

        @property
        def class_display_name(self):
            """
            Return const access to the name of the device's class name as displayed in Live's browser and device chain
            """
            pass

        @property
        def class_name(self):
            """
            Return const access to the name of the device's class.
            """
            pass

        @property
        def is_active(self):
            """
            Return const access to whether this device is active. This will be false bothwhen the device is off and when it's inside a rack device which is off.
            """
            pass

        @property
        def name(self):
            """
            Return access to the name of the device.
            """
            pass

        @property
        def parameters(self):
            """
            Const access to the list of available automatable parameters for this device.
            """
            pass

        @property
        def presets(self):
            """
            Get the list of presets the plugin offers.
            """
            pass

        @property
        def selected_preset_index(self):
            """
            Access to the index of the currently selected preset.
            """
            pass

        @property
        def type(self):
            """
            Return the type of the device.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a device.
            """
            pass

        def add_is_active_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_active" has changed. C++ signature :  void add_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_parameters_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "parameters" has changed. C++ signature :  void add_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_presets_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "presets" has changed. C++ signature :  void add_presets_listener(TPluginDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: PluginDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_selected_preset_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "selected_preset_index" has changed. C++ signature :  void add_selected_preset_index_listener(TPluginDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: PluginDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def get_parameter_names(self, arg1, begin=0, end=-1):
            """
            Get the range of plugin parameter names, bound by begin and end. If end is smaller than 0 it is interpreted as the parameter count.  C++ signature :  std::__1::vector<TString, std::__1::allocator<TString> > get_parameter_names(TPluginDevicePyHandle [,int=0 [,int=-1]])
            :param arg1: arg1
            :type arg1: PluginDevice
            :param begin: begin defaults to 0 
            :type begin: int
            :param end: end defaults to -1 
            :type end: int
            :rtype: StringVector
            """
            pass

        def is_active_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_active". C++ signature :  bool is_active_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def parameters_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "parameters". C++ signature :  bool parameters_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def presets_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "presets". C++ signature :  bool presets_has_listener(TPluginDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: PluginDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_is_active_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_active". C++ signature :  void remove_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_parameters_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "parameters". C++ signature :  void remove_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_presets_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "presets". C++ signature :  void remove_presets_listener(TPluginDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: PluginDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_selected_preset_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "selected_preset_index". C++ signature :  void remove_selected_preset_index_listener(TPluginDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: PluginDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def selected_preset_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "selected_preset_index". C++ signature :  bool selected_preset_index_has_listener(TPluginDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: PluginDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def store_chosen_bank(self, arg1, arg2, arg3):
            """
            Set the selected bank in the device for persistency. C++ signature :  void store_chosen_bank(TPyHandle<ADevice>,int,int)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a device.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the View.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the device is shown collapsed in the device chain.
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass


class RackDevice(ModuleType):
    pass

    class RackDevice(object):
        def __init__(self, *a, *k):
            """
            This class represents a Rack device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def can_have_chains(self):
            """
            Returns true if the device is a rack.
            """
            pass

        @property
        def can_have_drum_pads(self):
            """
            Returns true if the device is a drum rack.
            """
            pass

        @property
        def can_show_chains(self):
            """
            return True, if this Rack contains a rack instrument device that is capable of showing its chains in session view.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Device.
            """
            pass

        @property
        def chains(self):
            """
            Return const access to the list of chains in this device. Throws an exception if can_have_chains is false.
            """
            pass

        @property
        def class_display_name(self):
            """
            Return const access to the name of the device's class name as displayed in Live's browser and device chain
            """
            pass

        @property
        def class_name(self):
            """
            Return const access to the name of the device's class.
            """
            pass

        @property
        def drum_pads(self):
            """
            Return const access to the list of drum pads in this device. Throws an exception if can_have_drum_pads is false.
            """
            pass

        @property
        def has_drum_pads(self):
            """
            Returns true if the device is a drum rack which has drum pads. Throws an exception if can_have_drum_pads is false.
            """
            pass

        @property
        def has_macro_mappings(self):
            """
            Returns true if any of the rack's macros are mapped to a parameter.
            """
            pass

        @property
        def is_active(self):
            """
            Return const access to whether this device is active. This will be false bothwhen the device is off and when it's inside a rack device which is off.
            """
            pass

        @property
        def is_showing_chains(self):
            """
            Returns True, if it is showing chains.
            """
            pass

        @property
        def macros_mapped(self):
            """
            A list of booleans, one for each macro parameter, which is True iffthat macro is mapped to something
            """
            pass

        @property
        def name(self):
            """
            Return access to the name of the device.
            """
            pass

        @property
        def parameters(self):
            """
            Const access to the list of available automatable parameters for this device.
            """
            pass

        @property
        def return_chains(self):
            """
            Return const access to the list of return chains in this device. Throws an exception if can_have_chains is false.
            """
            pass

        @property
        def selected_variation_index(self):
            """
            Access to the index of the currently selected macro variation.Throws an exception if the index is out of range.
            """
            pass

        @property
        def type(self):
            """
            Return the type of the device.
            """
            pass

        @property
        def variation_count(self):
            """
            Access to the number of macro variations currently stored.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a device.
            """
            pass

        @property
        def visible_drum_pads(self):
            """
            Return const access to the list of visible drum pads in this device. Throws an exception if can_have_drum_pads is false.
            """
            pass

        def add_chains_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "chains" has changed. C++ signature :  void add_chains_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_drum_pads_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "drum_pads" has changed. C++ signature :  void add_drum_pads_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_has_drum_pads_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "has_drum_pads" has changed. C++ signature :  void add_has_drum_pads_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_has_macro_mappings_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "has_macro_mappings" has changed. C++ signature :  void add_has_macro_mappings_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_active_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_active" has changed. C++ signature :  void add_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_showing_chains_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_showing_chains" has changed. C++ signature :  void add_is_showing_chains_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_macro(self, arg1):
            """
            Increases the number of visible macro controls in the rack. Throws an exception if the maximum number of macro controls is reached. C++ signature :  void add_macro(TRackDevicePyHandle)
            :param arg1: arg1
            :type arg1: RackDevice
            """
            pass

        def add_macros_mapped_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "macros_mapped" has changed. C++ signature :  void add_macros_mapped_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_parameters_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "parameters" has changed. C++ signature :  void add_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_return_chains_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "return_chains" has changed. C++ signature :  void add_return_chains_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_visible_drum_pads_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "visible_drum_pads" has changed. C++ signature :  void add_visible_drum_pads_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def chains_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "chains". C++ signature :  bool chains_has_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def copy_pad(self, arg1, arg2, arg3):
            """
            Copies all contents of a drum pad from a source pad into a destination pad. copy_pad(source_index, destination_index) where source_index and destination_index correspond to the note number/index of the drum pad in a drum rack. Throws an exception when the source pad is empty, or when the source or destination indices are not between 0 - 127. C++ signature :  void copy_pad(TRackDevicePyHandle,int,int)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        def delete_selected_variation(self, arg1):
            """
            Deletes the currently selected macro variation.Does nothing if there is no selected variation. C++ signature :  void delete_selected_variation(TPyHandle<ADevice>)
            :param arg1: arg1
            :type arg1: Device
            """
            pass

        def drum_pads_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "drum_pads". C++ signature :  bool drum_pads_has_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def has_drum_pads_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "has_drum_pads". C++ signature :  bool has_drum_pads_has_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def has_macro_mappings_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "has_macro_mappings". C++ signature :  bool has_macro_mappings_has_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_active_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_active". C++ signature :  bool is_active_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_showing_chains_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_showing_chains". C++ signature :  bool is_showing_chains_has_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def macros_mapped_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "macros_mapped". C++ signature :  bool macros_mapped_has_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def parameters_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "parameters". C++ signature :  bool parameters_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def randomize_macros(self, arg1):
            """
            Randomizes the values for all macro controls not excluded from randomization. C++ signature :  void randomize_macros(TRackDevicePyHandle)
            :param arg1: arg1
            :type arg1: RackDevice
            """
            pass

        def recall_last_used_variation(self, arg1):
            """
            Recalls the macro variation that was recalled most recently.Does nothing if no variation has been recalled yet. C++ signature :  void recall_last_used_variation(TPyHandle<ADevice>)
            :param arg1: arg1
            :type arg1: Device
            """
            pass

        def recall_selected_variation(self, arg1):
            """
            Recalls the currently selected macro variation.Does nothing if there are no variations. C++ signature :  void recall_selected_variation(TPyHandle<ADevice>)
            :param arg1: arg1
            :type arg1: Device
            """
            pass

        def remove_chains_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "chains". C++ signature :  void remove_chains_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_drum_pads_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "drum_pads". C++ signature :  void remove_drum_pads_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_has_drum_pads_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "has_drum_pads". C++ signature :  void remove_has_drum_pads_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_has_macro_mappings_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "has_macro_mappings". C++ signature :  void remove_has_macro_mappings_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_active_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_active". C++ signature :  void remove_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_showing_chains_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_showing_chains". C++ signature :  void remove_is_showing_chains_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_macro(self, arg1):
            """
            Decreases the number of visible macro controls in the rack. Throws an exception if the minimum number of macro controls is reached. C++ signature :  void remove_macro(TRackDevicePyHandle)
            :param arg1: arg1
            :type arg1: RackDevice
            """
            pass

        def remove_macros_mapped_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "macros_mapped". C++ signature :  void remove_macros_mapped_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_parameters_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "parameters". C++ signature :  void remove_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_return_chains_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "return_chains". C++ signature :  void remove_return_chains_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_visible_drum_pads_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "visible_drum_pads". C++ signature :  void remove_visible_drum_pads_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def return_chains_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "return_chains". C++ signature :  bool return_chains_has_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def store_chosen_bank(self, arg1, arg2, arg3):
            """
            Set the selected bank in the device for persistency. C++ signature :  void store_chosen_bank(TPyHandle<ADevice>,int,int)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        def store_variation(self, arg1):
            """
            Stores a new variation of the values of all currently mapped macros C++ signature :  void store_variation(TPyHandle<ADevice>)
            :param arg1: arg1
            :type arg1: Device
            """
            pass

        def visible_drum_pads_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "visible_drum_pads". C++ signature :  bool visible_drum_pads_has_listener(TRackDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: RackDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a rack device.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the View.
                """
                pass

            @property
            def drum_pads_scroll_position(self):
                """
                Access to the index of the lowest visible row of pads. Throws an exception if can_have_drum_pads is false.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the device is shown collapsed in the device chain.
                """
                pass

            @property
            def is_showing_chain_devices(self):
                """
                Return whether the devices in the currently selected chain are visible. Throws an exception if can_have_chains is false.
                """
                pass

            @property
            def selected_chain(self):
                """
                Return access to the currently selected chain.
                """
                pass

            @property
            def selected_drum_pad(self):
                """
                Return access to the currently selected drum pad. Throws an exception if can_have_drum_pads is false.
                """
                pass

            def add_drum_pads_scroll_position_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "drum_pads_scroll_position" has changed. C++ signature :  void add_drum_pads_scroll_position_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_is_showing_chain_devices_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_showing_chain_devices" has changed. C++ signature :  void add_is_showing_chain_devices_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_selected_chain_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "selected_chain" has changed. C++ signature :  void add_selected_chain_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_selected_drum_pad_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "selected_drum_pad" has changed. C++ signature :  void add_selected_drum_pad_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def drum_pads_scroll_position_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "drum_pads_scroll_position". C++ signature :  bool drum_pads_scroll_position_has_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def is_showing_chain_devices_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_showing_chain_devices". C++ signature :  bool is_showing_chain_devices_has_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_drum_pads_scroll_position_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "drum_pads_scroll_position". C++ signature :  void remove_drum_pads_scroll_position_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_is_showing_chain_devices_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_showing_chain_devices". C++ signature :  void remove_is_showing_chain_devices_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_selected_chain_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "selected_chain". C++ signature :  void remove_selected_chain_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_selected_drum_pad_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "selected_drum_pad". C++ signature :  void remove_selected_drum_pad_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def selected_chain_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "selected_chain". C++ signature :  bool selected_chain_has_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def selected_drum_pad_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "selected_drum_pad". C++ signature :  bool selected_drum_pad_has_listener(TRackDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass


class Sample(ModuleType):
    pass

    class Sample(object):
        def __init__(self, *a, *k):
            """
            This class represents a sample file loaded into a Simpler instance.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def beats_granulation_resolution(self):
            """
            Access to the Granulation Resolution parameter in Beats Warp Mode.
            """
            pass

        @property
        def beats_transient_envelope(self):
            """
            Access to the Transient Envelope parameter in Beats Warp Mode.
            """
            pass

        @property
        def beats_transient_loop_mode(self):
            """
            Access to the Transient Loop Mode parameter in Beats Warp Mode.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Access to the sample's canonical parent.
            """
            pass

        @property
        def complex_pro_envelope(self):
            """
            Access to the Envelope parameter in Complex Pro Mode.
            """
            pass

        @property
        def complex_pro_formants(self):
            """
            Access to the Formants parameter in Complex Pro Warp Mode.
            """
            pass

        @property
        def end_marker(self):
            """
            Access to the position of the sample's end marker.
            """
            pass

        @property
        def file_path(self):
            """
            Get the path of the sample file.
            """
            pass

        @property
        def gain(self):
            """
            Access to the sample gain.
            """
            pass

        @property
        def length(self):
            """
            Get the length of the sample file in sample frames.
            """
            pass

        @property
        def sample_rate(self):
            """
            Access to the audio sample rate of the sample.
            """
            pass

        @property
        def slices(self):
            """
            Access to the list of slice points in sample time in the sample.
            """
            pass

        @property
        def slicing_beat_division(self):
            """
            Access to sample's slicing step size.
            """
            pass

        @property
        def slicing_region_count(self):
            """
            Access to sample's slicing split count.
            """
            pass

        @property
        def slicing_sensitivity(self):
            """
            Access to sample's slicing sensitivity whose sensitivity is in between 0.0 and 1.0.The higher the sensitivity, the more slices will be available.
            """
            pass

        @property
        def slicing_style(self):
            """
            Access to sample's slicing style.
            """
            pass

        @property
        def start_marker(self):
            """
            Access to the position of the sample's start marker.
            """
            pass

        @property
        def texture_flux(self):
            """
            Access to the Flux parameter in Texture Warp Mode.
            """
            pass

        @property
        def texture_grain_size(self):
            """
            Access to the Grain Size parameter in Texture Warp Mode.
            """
            pass

        @property
        def tones_grain_size(self):
            """
            Access to the Grain Size parameter in Tones Warp Mode.
            """
            pass

        @property
        def warp_markers(self):
            """
            Get the warp markers for this sample.
            """
            pass

        @property
        def warp_mode(self):
            """
            Access to the sample's warp mode.
            """
            pass

        @property
        def warping(self):
            """
            Access to the sample's warping property.
            """
            pass

        def add_beats_granulation_resolution_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "beats_granulation_resolution" has changed. C++ signature :  void add_beats_granulation_resolution_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_beats_transient_envelope_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "beats_transient_envelope" has changed. C++ signature :  void add_beats_transient_envelope_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_beats_transient_loop_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "beats_transient_loop_mode" has changed. C++ signature :  void add_beats_transient_loop_mode_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_complex_pro_envelope_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "complex_pro_envelope" has changed. C++ signature :  void add_complex_pro_envelope_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_complex_pro_formants_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "complex_pro_formants" has changed. C++ signature :  void add_complex_pro_formants_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_end_marker_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "end_marker" has changed. C++ signature :  void add_end_marker_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_file_path_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "file_path" has changed. C++ signature :  void add_file_path_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_gain_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "gain" has changed. C++ signature :  void add_gain_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_slices_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "slices" has changed. C++ signature :  void add_slices_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_slicing_beat_division_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "slicing_beat_division" has changed. C++ signature :  void add_slicing_beat_division_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_slicing_region_count_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "slicing_region_count" has changed. C++ signature :  void add_slicing_region_count_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_slicing_sensitivity_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "slicing_sensitivity" has changed. C++ signature :  void add_slicing_sensitivity_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_slicing_style_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "slicing_style" has changed. C++ signature :  void add_slicing_style_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_start_marker_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "start_marker" has changed. C++ signature :  void add_start_marker_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_texture_flux_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "texture_flux" has changed. C++ signature :  void add_texture_flux_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_texture_grain_size_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "texture_grain_size" has changed. C++ signature :  void add_texture_grain_size_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_tones_grain_size_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "tones_grain_size" has changed. C++ signature :  void add_tones_grain_size_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_warp_markers_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "warp_markers" has changed. C++ signature :  void add_warp_markers_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_warp_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "warp_mode" has changed. C++ signature :  void add_warp_mode_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_warping_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "warping" has changed. C++ signature :  void add_warping_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def beat_to_sample_time(self, handle, beat_time):
            """
            Converts the given beat time to sample time. Raises an error if the sample is not warped. C++ signature :  double beat_to_sample_time(TPyHandle<AMultiSamplePart>,double)
            :param handle: handle
            :type handle: Sample
            :param beat_time: beat_time
            :type beat_time: float
            :rtype: float
            """
            pass

        def beats_granulation_resolution_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "beats_granulation_resolution". C++ signature :  bool beats_granulation_resolution_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def beats_transient_envelope_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "beats_transient_envelope". C++ signature :  bool beats_transient_envelope_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def beats_transient_loop_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "beats_transient_loop_mode". C++ signature :  bool beats_transient_loop_mode_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def clear_slices(self, handle):
            """
            Clears all slices created in Simpler's manual mode. C++ signature :  void clear_slices(TPyHandle<AMultiSamplePart>)
            :param handle: handle
            :type handle: Sample
            """
            pass

        def complex_pro_envelope_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "complex_pro_envelope". C++ signature :  bool complex_pro_envelope_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def complex_pro_formants_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "complex_pro_formants". C++ signature :  bool complex_pro_formants_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def end_marker_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "end_marker". C++ signature :  bool end_marker_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def file_path_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "file_path". C++ signature :  bool file_path_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def gain_display_string(self, handle):
            """
            Get the gain's display value as a string. C++ signature :  TString gain_display_string(TPyHandle<AMultiSamplePart>)
            :param handle: handle
            :type handle: Sample
            :rtype: unicode
            """
            pass

        def gain_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "gain". C++ signature :  bool gain_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def insert_slice(self, handle, slice_time):
            """
            Add a slice point at the provided time if there is none. C++ signature :  void insert_slice(TPyHandle<AMultiSamplePart>,int)
            :param handle: handle
            :type handle: Sample
            :param slice_time: slice_time
            :type slice_time: int
            """
            pass

        def move_slice(self, handle, old_time, new_time):
            """
            Move the slice point at the provided time. C++ signature :  int move_slice(TPyHandle<AMultiSamplePart>,int,int)
            :param handle: handle
            :type handle: Sample
            :param old_time: old_time
            :type old_time: int
            :param new_time: new_time
            :type new_time: int
            :rtype: int
            """
            pass

        def remove_beats_granulation_resolution_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "beats_granulation_resolution". C++ signature :  void remove_beats_granulation_resolution_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_beats_transient_envelope_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "beats_transient_envelope". C++ signature :  void remove_beats_transient_envelope_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_beats_transient_loop_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "beats_transient_loop_mode". C++ signature :  void remove_beats_transient_loop_mode_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_complex_pro_envelope_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "complex_pro_envelope". C++ signature :  void remove_complex_pro_envelope_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_complex_pro_formants_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "complex_pro_formants". C++ signature :  void remove_complex_pro_formants_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_end_marker_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "end_marker". C++ signature :  void remove_end_marker_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_file_path_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "file_path". C++ signature :  void remove_file_path_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_gain_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "gain". C++ signature :  void remove_gain_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_slice(self, handle, slice_time):
            """
            Remove the slice point at the provided time if there is one. C++ signature :  void remove_slice(TPyHandle<AMultiSamplePart>,int)
            :param handle: handle
            :type handle: Sample
            :param slice_time: slice_time
            :type slice_time: int
            """
            pass

        def remove_slices_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "slices". C++ signature :  void remove_slices_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_slicing_beat_division_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "slicing_beat_division". C++ signature :  void remove_slicing_beat_division_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_slicing_region_count_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "slicing_region_count". C++ signature :  void remove_slicing_region_count_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_slicing_sensitivity_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "slicing_sensitivity". C++ signature :  void remove_slicing_sensitivity_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_slicing_style_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "slicing_style". C++ signature :  void remove_slicing_style_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_start_marker_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "start_marker". C++ signature :  void remove_start_marker_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_texture_flux_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "texture_flux". C++ signature :  void remove_texture_flux_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_texture_grain_size_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "texture_grain_size". C++ signature :  void remove_texture_grain_size_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_tones_grain_size_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "tones_grain_size". C++ signature :  void remove_tones_grain_size_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_warp_markers_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "warp_markers". C++ signature :  void remove_warp_markers_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_warp_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "warp_mode". C++ signature :  void remove_warp_mode_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_warping_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "warping". C++ signature :  void remove_warping_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def reset_slices(self, handle):
            """
            Resets all edited slices to their original positions. C++ signature :  void reset_slices(TPyHandle<AMultiSamplePart>)
            :param handle: handle
            :type handle: Sample
            """
            pass

        def sample_to_beat_time(self, handle, sample_time):
            """
            Converts the given sample time to beat time. Raises an error if the sample is not warped. C++ signature :  double sample_to_beat_time(TPyHandle<AMultiSamplePart>,double)
            :param handle: handle
            :type handle: Sample
            :param sample_time: sample_time
            :type sample_time: float
            :rtype: float
            """
            pass

        def slices_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "slices". C++ signature :  bool slices_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def slicing_beat_division_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "slicing_beat_division". C++ signature :  bool slicing_beat_division_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def slicing_region_count_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "slicing_region_count". C++ signature :  bool slicing_region_count_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def slicing_sensitivity_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "slicing_sensitivity". C++ signature :  bool slicing_sensitivity_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def slicing_style_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "slicing_style". C++ signature :  bool slicing_style_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def start_marker_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "start_marker". C++ signature :  bool start_marker_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def texture_flux_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "texture_flux". C++ signature :  bool texture_flux_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def texture_grain_size_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "texture_grain_size". C++ signature :  bool texture_grain_size_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def tones_grain_size_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "tones_grain_size". C++ signature :  bool tones_grain_size_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def warp_markers_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "warp_markers". C++ signature :  bool warp_markers_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def warp_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "warp_mode". C++ signature :  bool warp_mode_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def warping_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "warping". C++ signature :  bool warping_has_listener(TPyHandle<AMultiSamplePart>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Sample
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

    class SlicingBeatDivision(object):
        def __init__(self, *a, *k):
            pass

        @property
        def eighth(self):
            pass

        @property
        def eighth_triplett(self):
            pass

        @property
        def four_bars(self):
            pass

        @property
        def half(self):
            pass

        @property
        def half_triplett(self):
            pass

        @property
        def one_bar(self):
            pass

        @property
        def quarter(self):
            pass

        @property
        def quarter_triplett(self):
            pass

        @property
        def sixteenth(self):
            pass

        @property
        def sixteenth_triplett(self):
            pass

        @property
        def two_bars(self):
            pass

    class SlicingStyle(object):
        def __init__(self, *a, *k):
            pass

        @property
        def beat(self):
            pass

        @property
        def manual(self):
            pass

        @property
        def region(self):
            pass

        @property
        def transient(self):
            pass

    class TransientLoopMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def alternate(self):
            pass

        @property
        def forward(self):
            pass

        @property
        def off(self):
            pass


class Scene(ModuleType):
    pass

    class Scene(object):
        def __init__(self, *a, *k):
            """
            This class represents an series of ClipSlots in Lives Sessionview matrix.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the scene.
            """
            pass

        @property
        def clip_slots(self):
            """
            return a list of clipslots (see class AClipSlot) that this scene covers.
            """
            pass

        @property
        def color(self):
            """
            Get/set access to the color of the Scene (RGB).
            """
            pass

        @property
        def color_index(self):
            """
            Get/set access to the color index of the Scene. Can be None for no color.
            """
            pass

        @property
        def is_empty(self):
            """
            Returns True if all clip slots of this scene are empty.
            """
            pass

        @property
        def is_triggered(self):
            """
            Const access to the scene's trigger state.
            """
            pass

        @property
        def name(self):
            """
            Get/Set the name of the scene. Might contain the substring BPM, whichidentifies that the scene will change the tempo when fired. To Get/Setthe temp, use the 'tempo' property of the scene.
            """
            pass

        @property
        def tempo(self):
            """
            Get/Set the tempo value of the scene.The Song will use the Scenes tempo as soon as the Scene is fired.Returns -1 if the Scene has no tempo property.
            """
            pass

        def add_clip_slots_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "clip_slots" has changed. C++ signature :  void add_clip_slots_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_color_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color_index" has changed. C++ signature :  void add_color_index_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_color_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color" has changed. C++ signature :  void add_color_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_triggered_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_triggered" has changed. C++ signature :  void add_is_triggered_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def clip_slots_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "clip_slots". C++ signature :  bool clip_slots_has_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def color_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color". C++ signature :  bool color_has_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def color_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color_index". C++ signature :  bool color_index_has_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def fire(self, arg1, force_legato=False, can_select_scene_on_launch=True):
            """
            Fire the scene directly. Will fire all clipslots that this scene owns and select the scene itself. C++ signature :  void fire(TPyHandle<AScene> [,bool=False [,bool=True]])
            :param arg1: arg1
            :type arg1: Scene
            :param force_legato: force_legato defaults to False 
            :type force_legato: bool
            :param can_select_scene_on_launch: can_select_scene_on_launch defaults to True 
            :type can_select_scene_on_launch: bool
            """
            pass

        def fire_as_selected(self, arg1, force_legato=False):
            """
            Fire the selected scene. Will fire all clipslots that this scene owns and select the next scene if necessary. C++ signature :  void fire_as_selected(TPyHandle<AScene> [,bool=False])
            :param arg1: arg1
            :type arg1: Scene
            :param force_legato: force_legato defaults to False 
            :type force_legato: bool
            """
            pass

        def is_triggered_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_triggered". C++ signature :  bool is_triggered_has_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_clip_slots_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "clip_slots". C++ signature :  void remove_clip_slots_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_color_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color_index". C++ signature :  void remove_color_index_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_color_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color". C++ signature :  void remove_color_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_triggered_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_triggered". C++ signature :  void remove_is_triggered_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<AScene>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def set_fire_button_state(self, arg1, arg2):
            """
            Set the scene's fire button state directly. Supports all launch modes. C++ signature :  void set_fire_button_state(TPyHandle<AScene>,bool)
            :param arg1: arg1
            :type arg1: Scene
            :param arg2: arg2
            :type arg2: bool
            """
            pass


class SimplerDevice(ModuleType):
    pass

    @staticmethod
    def get_available_voice_numbers():
        """
        Get a vector of valid Simpler voice numbers. C++ signature :  std::__1::vector<int, std::__1::allocator<int> > get_available_voice_numbers()
        """
        pass

    class PlaybackMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def classic(self):
            pass

        @property
        def one_shot(self):
            pass

        @property
        def slicing(self):
            pass

    class SimplerDevice(object):
        def __init__(self, *a, *k):
            """
            This class represents a Simpler device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def can_have_chains(self):
            """
            Returns true if the device is a rack.
            """
            pass

        @property
        def can_have_drum_pads(self):
            """
            Returns true if the device is a drum rack.
            """
            pass

        @property
        def can_warp_as(self):
            """
            Returns true if warp_as is available.
            """
            pass

        @property
        def can_warp_double(self):
            """
            Returns true if warp_double is available.
            """
            pass

        @property
        def can_warp_half(self):
            """
            Returns true if warp_half is available.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Device.
            """
            pass

        @property
        def class_display_name(self):
            """
            Return const access to the name of the device's class name as displayed in Live's browser and device chain
            """
            pass

        @property
        def class_name(self):
            """
            Return const access to the name of the device's class.
            """
            pass

        @property
        def is_active(self):
            """
            Return const access to whether this device is active. This will be false bothwhen the device is off and when it's inside a rack device which is off.
            """
            pass

        @property
        def multi_sample_mode(self):
            """
            Returns whether Simpler is in mulit-sample mode.
            """
            pass

        @property
        def name(self):
            """
            Return access to the name of the device.
            """
            pass

        @property
        def pad_slicing(self):
            """
            When set to true, slices can be added in slicing mode by playing notes .that are not assigned to slices, yet.
            """
            pass

        @property
        def parameters(self):
            """
            Const access to the list of available automatable parameters for this device.
            """
            pass

        @property
        def playback_mode(self):
            """
            Access to Simpler's playback mode.
            """
            pass

        @property
        def playing_position(self):
            """
            Constant access to the current playing position in the sample.The returned value is the normalized position between sample start and end.
            """
            pass

        @property
        def playing_position_enabled(self):
            """
            Returns whether Simpler is showing the playing position.The returned value is True while the sample is played back
            """
            pass

        @property
        def retrigger(self):
            """
            Access to Simpler's retrigger mode.
            """
            pass

        @property
        def sample(self):
            """
            Get the loaded Sample.
            """
            pass

        @property
        def slicing_playback_mode(self):
            """
            Access to Simpler's slicing playback mode.
            """
            pass

        @property
        def type(self):
            """
            Return the type of the device.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a device.
            """
            pass

        @property
        def voices(self):
            """
            Access to the number of voices in Simpler.
            """
            pass

        def add_can_warp_as_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "can_warp_as" has changed. C++ signature :  void add_can_warp_as_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_can_warp_double_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "can_warp_double" has changed. C++ signature :  void add_can_warp_double_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_can_warp_half_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "can_warp_half" has changed. C++ signature :  void add_can_warp_half_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_active_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_active" has changed. C++ signature :  void add_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_multi_sample_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "multi_sample_mode" has changed. C++ signature :  void add_multi_sample_mode_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_pad_slicing_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "pad_slicing" has changed. C++ signature :  void add_pad_slicing_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_parameters_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "parameters" has changed. C++ signature :  void add_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_playback_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "playback_mode" has changed. C++ signature :  void add_playback_mode_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_playing_position_enabled_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "playing_position_enabled" has changed. C++ signature :  void add_playing_position_enabled_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_playing_position_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "playing_position" has changed. C++ signature :  void add_playing_position_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_retrigger_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "retrigger" has changed. C++ signature :  void add_retrigger_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_sample_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "sample" has changed. C++ signature :  void add_sample_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_slicing_playback_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "slicing_playback_mode" has changed. C++ signature :  void add_slicing_playback_mode_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_voices_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "voices" has changed. C++ signature :  void add_voices_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def can_warp_as_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "can_warp_as". C++ signature :  bool can_warp_as_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def can_warp_double_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "can_warp_double". C++ signature :  bool can_warp_double_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def can_warp_half_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "can_warp_half". C++ signature :  bool can_warp_half_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def crop(self, handle):
            """
            Crop the loaded sample to the active area between start- and end marker. Calling this method on an empty simpler raises an error. C++ signature :  void crop(TSimplerDevicePyHandle)
            :param handle: handle
            :type handle: SimplerDevice
            """
            pass

        def guess_playback_length(self, handle):
            """
            Return an estimated beat time for the playback length between start- and end-marker. Calling this method on an empty simpler raises an error. C++ signature :  double guess_playback_length(TSimplerDevicePyHandle)
            :param handle: handle
            :type handle: SimplerDevice
            :rtype: float
            """
            pass

        def is_active_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_active". C++ signature :  bool is_active_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def multi_sample_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "multi_sample_mode". C++ signature :  bool multi_sample_mode_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def pad_slicing_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "pad_slicing". C++ signature :  bool pad_slicing_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def parameters_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "parameters". C++ signature :  bool parameters_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def playback_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "playback_mode". C++ signature :  bool playback_mode_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def playing_position_enabled_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "playing_position_enabled". C++ signature :  bool playing_position_enabled_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def playing_position_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "playing_position". C++ signature :  bool playing_position_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_can_warp_as_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "can_warp_as". C++ signature :  void remove_can_warp_as_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_can_warp_double_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "can_warp_double". C++ signature :  void remove_can_warp_double_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_can_warp_half_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "can_warp_half". C++ signature :  void remove_can_warp_half_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_active_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_active". C++ signature :  void remove_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_multi_sample_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "multi_sample_mode". C++ signature :  void remove_multi_sample_mode_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_pad_slicing_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "pad_slicing". C++ signature :  void remove_pad_slicing_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_parameters_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "parameters". C++ signature :  void remove_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_playback_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "playback_mode". C++ signature :  void remove_playback_mode_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_playing_position_enabled_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "playing_position_enabled". C++ signature :  void remove_playing_position_enabled_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_playing_position_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "playing_position". C++ signature :  void remove_playing_position_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_retrigger_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "retrigger". C++ signature :  void remove_retrigger_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_sample_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "sample". C++ signature :  void remove_sample_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_slicing_playback_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "slicing_playback_mode". C++ signature :  void remove_slicing_playback_mode_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_voices_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "voices". C++ signature :  void remove_voices_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def retrigger_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "retrigger". C++ signature :  bool retrigger_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def reverse(self, handle):
            """
            Reverse the loaded sample. Calling this method on an empty simpler raises an error. C++ signature :  void reverse(TSimplerDevicePyHandle)
            :param handle: handle
            :type handle: SimplerDevice
            """
            pass

        def sample_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "sample". C++ signature :  bool sample_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def slicing_playback_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "slicing_playback_mode". C++ signature :  bool slicing_playback_mode_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def store_chosen_bank(self, arg1, arg2, arg3):
            """
            Set the selected bank in the device for persistency. C++ signature :  void store_chosen_bank(TPyHandle<ADevice>,int,int)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        def voices_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "voices". C++ signature :  bool voices_has_listener(TSimplerDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: SimplerDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def warp_as(self, handle, beat_time):
            """
            Warp the playback region between start- and end-marker as the given length. Calling this method on an empty simpler raises an error. C++ signature :  void warp_as(TSimplerDevicePyHandle,double)
            :param handle: handle
            :type handle: SimplerDevice
            :param beat_time: beat_time
            :type beat_time: float
            """
            pass

        def warp_double(self, handle):
            """
            Doubles the tempo for region between start- and end-marker. C++ signature :  void warp_double(TSimplerDevicePyHandle)
            :param handle: handle
            :type handle: SimplerDevice
            """
            pass

        def warp_half(self, handle):
            """
            Halves the tempo for region between start- and end-marker. C++ signature :  void warp_half(TSimplerDevicePyHandle)
            :param handle: handle
            :type handle: SimplerDevice
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a simpler device.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the View.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the device is shown collapsed in the device chain.
                """
                pass

            @property
            def sample_end(self):
                """
                Access to the modulated samples end position in samples. Returns -1 in case there is no sample loaded.
                """
                pass

            @property
            def sample_env_fade_in(self):
                """
                Access to the envelope fade-in time in samples. Returned value is only in use when Simpler is in one-shot mode. Returns -1 in case there is no sample loaded.
                """
                pass

            @property
            def sample_env_fade_out(self):
                """
                Access to the envelope fade-out time in samples. Returned value is only in use when Simpler is in one-shot mode. Returns -1 in case there is no sample loaded.
                """
                pass

            @property
            def sample_loop_end(self):
                """
                Access to the modulated samples loop end position in samples. Returns -1 in case there is no sample loaded.
                """
                pass

            @property
            def sample_loop_fade(self):
                """
                Access to the modulated samples loop fade position in samples. Returns -1 in case there is no sample loaded.
                """
                pass

            @property
            def sample_loop_start(self):
                """
                Access to the modulated samples loop start position in samples. Returns -1 in case there is no sample loaded.
                """
                pass

            @property
            def sample_start(self):
                """
                Access to the modulated samples start position in samples. Returns -1 in case there is no sample loaded.
                """
                pass

            @property
            def selected_slice(self):
                """
                Access to the selected slice.
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_sample_end_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "sample_end" has changed. C++ signature :  void add_sample_end_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_sample_env_fade_in_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "sample_env_fade_in" has changed. C++ signature :  void add_sample_env_fade_in_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_sample_env_fade_out_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "sample_env_fade_out" has changed. C++ signature :  void add_sample_env_fade_out_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_sample_loop_end_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "sample_loop_end" has changed. C++ signature :  void add_sample_loop_end_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_sample_loop_fade_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "sample_loop_fade" has changed. C++ signature :  void add_sample_loop_fade_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_sample_loop_start_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "sample_loop_start" has changed. C++ signature :  void add_sample_loop_start_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_sample_start_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "sample_start" has changed. C++ signature :  void add_sample_start_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_selected_slice_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "selected_slice" has changed. C++ signature :  void add_selected_slice_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_sample_end_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "sample_end". C++ signature :  void remove_sample_end_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_sample_env_fade_in_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "sample_env_fade_in". C++ signature :  void remove_sample_env_fade_in_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_sample_env_fade_out_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "sample_env_fade_out". C++ signature :  void remove_sample_env_fade_out_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_sample_loop_end_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "sample_loop_end". C++ signature :  void remove_sample_loop_end_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_sample_loop_fade_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "sample_loop_fade". C++ signature :  void remove_sample_loop_fade_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_sample_loop_start_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "sample_loop_start". C++ signature :  void remove_sample_loop_start_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_sample_start_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "sample_start". C++ signature :  void remove_sample_start_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_selected_slice_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "selected_slice". C++ signature :  void remove_selected_slice_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def sample_end_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "sample_end". C++ signature :  bool sample_end_has_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def sample_env_fade_in_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "sample_env_fade_in". C++ signature :  bool sample_env_fade_in_has_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def sample_env_fade_out_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "sample_env_fade_out". C++ signature :  bool sample_env_fade_out_has_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def sample_loop_end_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "sample_loop_end". C++ signature :  bool sample_loop_end_has_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def sample_loop_fade_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "sample_loop_fade". C++ signature :  bool sample_loop_fade_has_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def sample_loop_start_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "sample_loop_start". C++ signature :  bool sample_loop_start_has_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def sample_start_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "sample_start". C++ signature :  bool sample_start_has_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def selected_slice_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "selected_slice". C++ signature :  bool selected_slice_has_listener(TSimplerDevicePyViewData,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

    class SlicingPlaybackMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def mono(self):
            pass

        @property
        def poly(self):
            pass

        @property
        def thru(self):
            pass


class Song(ModuleType):
    pass

    @staticmethod
    def get_all_scales_ordered():
        """
        Get an ordered tuple of tuples of all available scale names to intervals. C++ signature :  boost::python::tuple get_all_scales_ordered()
        """
        pass

    class BeatTime(object):
        def __init__(self, *a, *k):
            """
            Represents a Time, splitted into Bars, Beats, SubDivision and Ticks.
            """
            pass

        @property
        def bars(self):
            pass

        @property
        def beats(self):
            pass

        @property
        def sub_division(self):
            pass

        @property
        def ticks(self):
            pass

    class CaptureDestination(object):
        def __init__(self, *a, *k):
            """
            The destination for MIDI capture.
            """
            pass

        @property
        def arrangement(self):
            """
            The destination for MIDI capture.
            """
            pass

        @property
        def auto(self):
            """
            The destination for MIDI capture.
            """
            pass

        @property
        def session(self):
            """
            The destination for MIDI capture.
            """
            pass

    class CaptureMode(object):
        def __init__(self, *a, *k):
            """
            The capture mode that is used for capture and insert scene.
            """
            pass

        @property
        def all(self):
            """
            The capture mode that is used for capture and insert scene.
            """
            pass

        @property
        def all_except_selected(self):
            """
            The capture mode that is used for capture and insert scene.
            """
            pass

    class CuePoint(object):
        def __init__(self, *a, *k):
            """
            Represents a 'Marker' in the arrangement.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the cue point.
            """
            pass

        @property
        def name(self):
            """
            Get/Listen to the name of this CuePoint, as visible in the arranger.
            """
            pass

        @property
        def time(self):
            """
            Get/Listen to the CuePoint's time in beats.
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ACuePoint>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CuePoint
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_time_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "time" has changed. C++ signature :  void add_time_listener(TPyHandle<ACuePoint>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CuePoint
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def jump(self, arg1):
            """
            When the Song is playing, set the playing-position quantized to this Cuepoint's time. When not playing, simply move the start playing position. C++ signature :  void jump(TPyHandle<ACuePoint>)
            :param arg1: arg1
            :type arg1: CuePoint
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ACuePoint>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CuePoint
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ACuePoint>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CuePoint
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_time_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "time". C++ signature :  void remove_time_listener(TPyHandle<ACuePoint>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CuePoint
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def time_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "time". C++ signature :  bool time_has_listener(TPyHandle<ACuePoint>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: CuePoint
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

    class Quantization(object):
        def __init__(self, *a, *k):
            pass

        @property
        def q_2_bars(self):
            pass

        @property
        def q_4_bars(self):
            pass

        @property
        def q_8_bars(self):
            pass

        @property
        def q_bar(self):
            pass

        @property
        def q_eight(self):
            pass

        @property
        def q_eight_triplet(self):
            pass

        @property
        def q_half(self):
            pass

        @property
        def q_half_triplet(self):
            pass

        @property
        def q_no_q(self):
            pass

        @property
        def q_quarter(self):
            pass

        @property
        def q_quarter_triplet(self):
            pass

        @property
        def q_sixtenth(self):
            pass

        @property
        def q_sixtenth_triplet(self):
            pass

        @property
        def q_thirtytwoth(self):
            pass

    class RecordingQuantization(object):
        def __init__(self, *a, *k):
            pass

        @property
        def rec_q_eight(self):
            pass

        @property
        def rec_q_eight_eight_triplet(self):
            pass

        @property
        def rec_q_eight_triplet(self):
            pass

        @property
        def rec_q_no_q(self):
            pass

        @property
        def rec_q_quarter(self):
            pass

        @property
        def rec_q_sixtenth(self):
            pass

        @property
        def rec_q_sixtenth_sixtenth_triplet(self):
            pass

        @property
        def rec_q_sixtenth_triplet(self):
            pass

        @property
        def rec_q_thirtysecond(self):
            pass

    class SessionRecordStatus(object):
        def __init__(self, *a, *k):
            pass

        @property
        def off(self):
            pass

        @property
        def on(self):
            pass

        @property
        def transition(self):
            pass

    class SmptTime(object):
        def __init__(self, *a, *k):
            """
            Represents a Time, split into Hours, Minutes, Seconds and Frames.The frame type must be specified when calling a function that returnsa SmptTime.
            """
            pass

        @property
        def frames(self):
            pass

        @property
        def hours(self):
            pass

        @property
        def minutes(self):
            pass

        @property
        def seconds(self):
            pass

    class Song(object):
        def __init__(self, *a, *k):
            """
            This class represents a Live set.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def appointed_device(self):
            """
            Read, write, and listen access to the appointed Device
            """
            pass

        @property
        def arrangement_overdub(self):
            """
            Get/Set the global arrangement overdub state.
            """
            pass

        @property
        def back_to_arranger(self):
            """
            Get/Set if triggering a Clip in the Session, disabled the playback ofClips in the Arranger.
            """
            pass

        @property
        def can_capture_midi(self):
            """
            Get whether there currently is material to be captured on any tracks.
            """
            pass

        @property
        def can_jump_to_next_cue(self):
            """
            Returns true when there is a cue marker right to the playing pos thatwe could jump to.
            """
            pass

        @property
        def can_jump_to_prev_cue(self):
            """
            Returns true when there is a cue marker left to the playing pos thatwe could jump to.
            """
            pass

        @property
        def can_redo(self):
            """
            Returns true if there is an undone action that we can redo.
            """
            pass

        @property
        def can_undo(self):
            """
            Returns true if there is an action that we can restore.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the song.
            """
            pass

        @property
        def clip_trigger_quantization(self):
            """
            Get/Set access to the quantization settings that are used to fireClips in the Session.
            """
            pass

        @property
        def count_in_duration(self):
            """
            Get the count in duration. Returns an index, mapped as follows: 0 - None, 1 - 1 Bar, 2 - 2 Bars, 3 - 4 Bars.
            """
            pass

        @property
        def cue_points(self):
            """
            Const access to a list of all cue points of the Live Song.
            """
            pass

        @property
        def current_song_time(self):
            """
            Get/Set access to the songs current playing position in ms.
            """
            pass

        @property
        def exclusive_arm(self):
            """
            Get if Tracks should be armed exclusively by default.
            """
            pass

        @property
        def exclusive_solo(self):
            """
            Get if Tracks should be soloed exclusively by default.
            """
            pass

        @property
        def groove_amount(self):
            """
            Get/Set the global groove amount, that adjust all setup groovesin all clips.
            """
            pass

        @property
        def groove_pool(self):
            """
            Get the groove pool.
            """
            pass

        @property
        def is_counting_in(self):
            """
            Get whether currently counting in.
            """
            pass

        @property
        def is_playing(self):
            """
            Returns true if the Song is currently playing.
            """
            pass

        @property
        def last_event_time(self):
            """
            Return the time of the last set event in the song. In contrary tosong_length, this will not add some extra beats that are mostly neededfor Display purposes in the Arrangerview.
            """
            pass

        @property
        def loop(self):
            """
            Get/Set the looping flag that en/disables the usage of the globalloop markers in the song.
            """
            pass

        @property
        def loop_length(self):
            """
            Get/Set the length of the global loop marker position in beats.
            """
            pass

        @property
        def loop_start(self):
            """
            Get/Set the start of the global loop marker position in beats.
            """
            pass

        @property
        def master_track(self):
            """
            Access to the Master Track (always available)
            """
            pass

        @property
        def metronome(self):
            """
            Get/Set if the metronom is audible.
            """
            pass

        @property
        def midi_recording_quantization(self):
            """
            Get/Set access to the settings that are used to quantizeMIDI recordings.
            """
            pass

        @property
        def nudge_down(self):
            """
            Get/Set the status of the nudge down button.
            """
            pass

        @property
        def nudge_up(self):
            """
            Get/Set the status of the nudge up button.
            """
            pass

        @property
        def overdub(self):
            """
            Legacy hook for Live 8 overdub state. Now hooks tosession record, but never starts playback.
            """
            pass

        @property
        def punch_in(self):
            """
            Get/Set the flag that will enable recording as soon as the Song playsand hits the global loop start region.
            """
            pass

        @property
        def punch_out(self):
            """
            Get/Set the flag that will disable recording as soon as the Song playsand hits the global loop end region.
            """
            pass

        @property
        def re_enable_automation_enabled(self):
            """
            Returns true if some automated parameter has been overriden
            """
            pass

        @property
        def record_mode(self):
            """
            Get/Set the state of the global recording flag.
            """
            pass

        @property
        def return_tracks(self):
            """
            Const access to the list of available Return Tracks.
            """
            pass

        @property
        def root_note(self):
            """
            Set and access the root note (i.e. key) of the song used for control surfaces. The root note can be a number between 0 and 11, with 0 corresponding to C and 11 corresponding to B.
            """
            pass

        @property
        def scale_intervals(self):
            """
            Reports the current scale's intervals as a list of integers, starting with the root note and representing the number of halfsteps (e.g. Major -> 0, 2, 4, 5, 7, 9, 11)
            """
            pass

        @property
        def scale_name(self):
            """
            Set and access the last used scale name for control surfaces. The default scale names that can be saved with a set and recalled are'Major', 'Minor', 'Dorian', 'Mixolydian' ,'Lydian' ,'Phrygian' ,'Locrian', 'Whole Tone', 'Half-whole Dim.', 'Whole-half Dim.', 'Minor Blues', 'Minor Pentatonic', 'Major Pentatonic', 'Harmonic Minor', 'Harmonic Major', 'Dorian #4', 'Phrygian Dominant', 'Melodic Minor', 'Lydian Augmented', 'Lydian Dominant', 'Super Locrian', 'Bhairav', 'Hungarian Minor', '8-Tone Spanish', 'Hirajoshi', 'In-Sen', 'Iwato', 'Kumoi', 'Pelog Selisir', 'Pelog Tembung', 'Messaien 3', 'Messaien 4', 'Messaien 5', 'Messaien 6', 'Messaien 7'
            """
            pass

        @property
        def scenes(self):
            """
            Const access to a list of all Scenes in the Live Song.
            """
            pass

        @property
        def select_on_launch(self):
            """
            Get if Scenes and Clips should be selected when fired.
            """
            pass

        @property
        def session_automation_record(self):
            """
            Returns true if automation recording is enabled.
            """
            pass

        @property
        def session_record(self):
            """
            Get/Set the session record state.
            """
            pass

        @property
        def session_record_status(self):
            """
            Get the session slot-recording state.
            """
            pass

        @property
        def signature_denominator(self):
            """
            Get/Set access to the global signature denominator of the Song.
            """
            pass

        @property
        def signature_numerator(self):
            """
            Get/Set access to the global signature numerator of the Song.
            """
            pass

        @property
        def song_length(self):
            """
            Return the time of the last set event in the song, plus som extra beatsthat are usually added for better navigation in the arrangerview.
            """
            pass

        @property
        def swing_amount(self):
            """
            Get/Set access to the amount of swing that is applied when adding or quantizing notes to MIDI clips
            """
            pass

        @property
        def tempo(self):
            """
            Get/Set the global project tempo.
            """
            pass

        @property
        def tracks(self):
            """
            Const access to a list of all Player Tracks in the Live Song, exludingthe return and Master Track (see also Song.send_tracks and Song.master_track).At least one MIDI or Audio Track is always available.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a Live document: The Session and Arrangerview.
            """
            pass

        @property
        def visible_tracks(self):
            """
            Const access to a list of all visible Player Tracks in the Live Song, exludingthe return and Master Track (see also Song.send_tracks and Song.master_track).At least one MIDI or Audio Track is always available.
            """
            pass

        def add_appointed_device_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "appointed_device" has changed. C++ signature :  void add_appointed_device_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_arrangement_overdub_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "arrangement_overdub" has changed. C++ signature :  void add_arrangement_overdub_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_back_to_arranger_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "back_to_arranger" has changed. C++ signature :  void add_back_to_arranger_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_can_capture_midi_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "can_capture_midi" has changed. C++ signature :  void add_can_capture_midi_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_can_jump_to_next_cue_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "can_jump_to_next_cue" has changed. C++ signature :  void add_can_jump_to_next_cue_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_can_jump_to_prev_cue_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "can_jump_to_prev_cue" has changed. C++ signature :  void add_can_jump_to_prev_cue_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_clip_trigger_quantization_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "clip_trigger_quantization" has changed. C++ signature :  void add_clip_trigger_quantization_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_count_in_duration_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "count_in_duration" has changed. C++ signature :  void add_count_in_duration_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_cue_points_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "cue_points" has changed. C++ signature :  void add_cue_points_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_current_song_time_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "current_song_time" has changed. C++ signature :  void add_current_song_time_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_data_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "data" has changed. C++ signature :  void add_data_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_exclusive_arm_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "exclusive_arm" has changed. C++ signature :  void add_exclusive_arm_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_groove_amount_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "groove_amount" has changed. C++ signature :  void add_groove_amount_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_counting_in_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_counting_in" has changed. C++ signature :  void add_is_counting_in_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_playing_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_playing" has changed. C++ signature :  void add_is_playing_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_loop_length_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "loop_length" has changed. C++ signature :  void add_loop_length_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_loop_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "loop" has changed. C++ signature :  void add_loop_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_loop_start_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "loop_start" has changed. C++ signature :  void add_loop_start_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_metronome_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "metronome" has changed. C++ signature :  void add_metronome_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_midi_recording_quantization_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "midi_recording_quantization" has changed. C++ signature :  void add_midi_recording_quantization_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_nudge_down_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "nudge_down" has changed. C++ signature :  void add_nudge_down_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_nudge_up_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "nudge_up" has changed. C++ signature :  void add_nudge_up_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_overdub_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "overdub" has changed. C++ signature :  void add_overdub_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_punch_in_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "punch_in" has changed. C++ signature :  void add_punch_in_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_punch_out_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "punch_out" has changed. C++ signature :  void add_punch_out_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_re_enable_automation_enabled_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "re_enable_automation_enabled" has changed. C++ signature :  void add_re_enable_automation_enabled_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_record_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "record_mode" has changed. C++ signature :  void add_record_mode_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_return_tracks_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "return_tracks" has changed. C++ signature :  void add_return_tracks_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_root_note_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "root_note" has changed. C++ signature :  void add_root_note_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_scale_intervals_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "scale_intervals" has changed. C++ signature :  void add_scale_intervals_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_scale_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "scale_name" has changed. C++ signature :  void add_scale_name_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_scenes_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "scenes" has changed. C++ signature :  void add_scenes_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_session_automation_record_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "session_automation_record" has changed. C++ signature :  void add_session_automation_record_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_session_record_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "session_record" has changed. C++ signature :  void add_session_record_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_session_record_status_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "session_record_status" has changed. C++ signature :  void add_session_record_status_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_signature_denominator_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "signature_denominator" has changed. C++ signature :  void add_signature_denominator_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_signature_numerator_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "signature_numerator" has changed. C++ signature :  void add_signature_numerator_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_song_length_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "song_length" has changed. C++ signature :  void add_song_length_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_swing_amount_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "swing_amount" has changed. C++ signature :  void add_swing_amount_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_tempo_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "tempo" has changed. C++ signature :  void add_tempo_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_tracks_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "tracks" has changed. C++ signature :  void add_tracks_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_visible_tracks_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "visible_tracks" has changed. C++ signature :  void add_visible_tracks_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def appointed_device_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "appointed_device". C++ signature :  bool appointed_device_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def arrangement_overdub_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "arrangement_overdub". C++ signature :  bool arrangement_overdub_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def back_to_arranger_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "back_to_arranger". C++ signature :  bool back_to_arranger_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def begin_undo_step(self, arg1):
            """
            C++ signature :  void begin_undo_step(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def can_capture_midi_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "can_capture_midi". C++ signature :  bool can_capture_midi_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def can_jump_to_next_cue_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "can_jump_to_next_cue". C++ signature :  bool can_jump_to_next_cue_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def can_jump_to_prev_cue_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "can_jump_to_prev_cue". C++ signature :  bool can_jump_to_prev_cue_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def capture_and_insert_scene(self, arg1, CaptureMode=Song.CaptureMode.all):
            """
            Capture currently playing clips and insert them as a new scene after the selected scene. Raises a runtime error if creating a new scene would exceed the limitations. C++ signature :  void capture_and_insert_scene(TPyHandle<ASong> [,int=Song.CaptureMode.all])
            :param arg1: arg1
            :type arg1: Song
            :param CaptureMode: CaptureMode defaults to Song.CaptureMode.all 
            :type CaptureMode: int
            """
            pass

        def capture_midi(self, arg1, Destination=Song.CaptureDestination.auto):
            """
            Capture recently played MIDI material from audible tracks. If no Destination is given or Destination is set to CaptureDestination.auto, the captured material is inserted into the Session or Arrangement depending on which is visible. If Destination is set to CaptureDestination.session or CaptureDestination.arrangement, inserts the material into Session or Arrangement, respectively. Raises a limitation error when capturing into the Session and a new scene would have to be created but can't because it would exceed the limitations. C++ signature :  void capture_midi(TPyHandle<ASong> [,int=Song.CaptureDestination.auto])
            :param arg1: arg1
            :type arg1: Song
            :param Destination: Destination defaults to Song.CaptureDestination.auto 
            :type Destination: int
            """
            pass

        def clip_trigger_quantization_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "clip_trigger_quantization". C++ signature :  bool clip_trigger_quantization_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def continue_playing(self, arg1):
            """
            Continue playing the song from the current position C++ signature :  void continue_playing(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def count_in_duration_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "count_in_duration". C++ signature :  bool count_in_duration_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def create_audio_track(self, arg1, Index=None):
            """
            Create a new audio track at the optional given index and return it.If the index is -1, the new track is added at the end. It will create a default audio track if possible. If the index is invalid or the new track would exceed the limitations, a limitation error is raised.If the index is missing, the track is created after the last selected item C++ signature :  TWeakPtr<TTrackPyHandle> create_audio_track(TPyHandle<ASong> [,boost::python::api::object=None])
            :param arg1: arg1
            :type arg1: Song
            :param Index: Index defaults to None 
            :type Index: object
            :rtype: Track
            """
            pass

        def create_midi_track(self, arg1, Index=None):
            """
            Create a new midi track at the optional given index and return it.If the index is -1,  the new track is added at the end.It will create a default midi track if possible. If the index is invalid or the new track would exceed the limitations, a limitation error is raised.If the index is missing, the track is created after the last selected item C++ signature :  TWeakPtr<TTrackPyHandle> create_midi_track(TPyHandle<ASong> [,boost::python::api::object=None])
            :param arg1: arg1
            :type arg1: Song
            :param Index: Index defaults to None 
            :type Index: object
            :rtype: Track
            """
            pass

        def create_return_track(self, arg1):
            """
            Create a new return track at the end and return it. If the new track would exceed  the limitations, a limitation error is raised.  If the maximum number of return tracks is exceeded, a RuntimeError is raised. C++ signature :  TWeakPtr<TTrackPyHandle> create_return_track(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            :rtype: Track
            """
            pass

        def create_scene(self, arg1, arg2):
            """
            Create a new scene at the given index. If the index is -1, the new scene is added at the end. If the index is invalid or the new scene would exceed the limitations, a limitation error is raised. C++ signature :  TWeakPtr<TPyHandle<AScene> > create_scene(TPyHandle<ASong>,int)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: int
            :rtype: Scene
            """
            pass

        def cue_points_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "cue_points". C++ signature :  bool cue_points_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def current_song_time_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "current_song_time". C++ signature :  bool current_song_time_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def data_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "data". C++ signature :  bool data_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def delete_return_track(self, arg1, arg2):
            """
            Delete the return track with the given index. If no track with this index exists, an exception will be raised. C++ signature :  void delete_return_track(TPyHandle<ASong>,int)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: int
            """
            pass

        def delete_scene(self, arg1, arg2):
            """
            Delete the scene with the given index. If no scene with this index exists, an exception will be raised. C++ signature :  void delete_scene(TPyHandle<ASong>,int)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: int
            """
            pass

        def delete_track(self, arg1, arg2):
            """
            Delete the track with the given index. If no track with this index exists, an exception will be raised. C++ signature :  void delete_track(TPyHandle<ASong>,int)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: int
            """
            pass

        def duplicate_scene(self, arg1, arg2):
            """
            Duplicates a scene and selects the new one. Raises a limitation error if creating a new scene would exceed the limitations. C++ signature :  void duplicate_scene(TPyHandle<ASong>,int)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: int
            """
            pass

        def duplicate_track(self, arg1, arg2):
            """
            Duplicates a track and selects the new one. If the track is inside a folded group track, the group track is unfolded. Raises a limitation error if creating a new track would exceed the limitations. C++ signature :  void duplicate_track(TPyHandle<ASong>,int)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: int
            """
            pass

        def end_undo_step(self, arg1):
            """
            C++ signature :  void end_undo_step(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def exclusive_arm_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "exclusive_arm". C++ signature :  bool exclusive_arm_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def find_device_position(self, arg1, device, target, target_position):
            """
            Returns the closest possible position to the given target, where the device can be inserted. If inserting is not possible at all (i.e. if the device type is wrong), -1 is returned. C++ signature :  int find_device_position(TPyHandle<ASong>,TPyHandle<ADevice>,TPyHandleBase,int)
            :param arg1: arg1
            :type arg1: Song
            :param device: device
            :type device: Device
            :param target: target
            :type target: LomObject
            :param target_position: target_position
            :type target_position: int
            :rtype: int
            """
            pass

        def force_link_beat_time(self, arg1):
            """
            Force the Link timeline to jump to Lives current beat time. Danger: This can cause beat time discontinuities in other connected apps. C++ signature :  void force_link_beat_time(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def get_beats_loop_length(self, arg1):
            """
            Get const access to the songs loop length, using a BeatTime class with the current global set signature. C++ signature :  NSongApi::TBeatTime get_beats_loop_length(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            :rtype: BeatTime
            """
            pass

        def get_beats_loop_start(self, arg1):
            """
            Get const access to the songs loop start, using a BeatTime class with the current global set signature. C++ signature :  NSongApi::TBeatTime get_beats_loop_start(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            :rtype: BeatTime
            """
            pass

        def get_current_beats_song_time(self, arg1):
            """
            Get const access to the songs current playing position, using a BeatTime class with the current global set signature. C++ signature :  NSongApi::TBeatTime get_current_beats_song_time(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            :rtype: BeatTime
            """
            pass

        def get_current_smpte_song_time(self, arg1, arg2):
            """
            Get const access to the songs current playing position, by specifying the SMPTE format in which you would like to receive the time. C++ signature :  NSongApi::TSmptTime get_current_smpte_song_time(TPyHandle<ASong>,int)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: int
            :rtype: SmptTime
            """
            pass

        def get_data(self, arg1, key, default_value):
            """
            Get data for the given key, that was previously stored using set_data. C++ signature :  boost::python::api::object get_data(TPyHandle<ASong>,TString,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param key: key
            :type key: object
            :param default_value: default_value
            :type default_value: object
            :rtype: object
            """
            pass

        def groove_amount_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "groove_amount". C++ signature :  bool groove_amount_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_counting_in_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_counting_in". C++ signature :  bool is_counting_in_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_cue_point_selected(self, arg1):
            """
            Return true if the global playing pos is currently on a cue point. C++ signature :  bool is_cue_point_selected(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            :rtype: bool
            """
            pass

        def is_playing_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_playing". C++ signature :  bool is_playing_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def jump_by(self, arg1, arg2):
            """
            Set a new playing pos, relative to the current one. C++ signature :  void jump_by(TPyHandle<ASong>,double)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: float
            """
            pass

        def jump_to_next_cue(self, arg1):
            """
            Jump to the next cue (marker) if possible. C++ signature :  void jump_to_next_cue(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def jump_to_prev_cue(self, arg1):
            """
            Jump to the prior cue (marker) if possible. C++ signature :  void jump_to_prev_cue(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def loop_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "loop". C++ signature :  bool loop_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def loop_length_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "loop_length". C++ signature :  bool loop_length_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def loop_start_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "loop_start". C++ signature :  bool loop_start_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def metronome_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "metronome". C++ signature :  bool metronome_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def midi_recording_quantization_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "midi_recording_quantization". C++ signature :  bool midi_recording_quantization_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def move_device(self, arg1, device, target, target_position):
            """
            Move a device into the target at the given position, where 0 moves it before the first device and len(devices) moves it to the end of the device chain.If the device cannot be moved to this position, the nearest possible position is chosen. If the device type is not valid, a runtime error is raised.Returns the index, where the device was moved to. C++ signature :  int move_device(TPyHandle<ASong>,TPyHandle<ADevice>,TPyHandleBase,int)
            :param arg1: arg1
            :type arg1: Song
            :param device: device
            :type device: Device
            :param target: target
            :type target: LomObject
            :param target_position: target_position
            :type target_position: int
            :rtype: int
            """
            pass

        def nudge_down_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "nudge_down". C++ signature :  bool nudge_down_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def nudge_up_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "nudge_up". C++ signature :  bool nudge_up_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def overdub_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "overdub". C++ signature :  bool overdub_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def play_selection(self, arg1):
            """
            Start playing the current set selection, or do nothing if no selection is set. C++ signature :  void play_selection(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def punch_in_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "punch_in". C++ signature :  bool punch_in_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def punch_out_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "punch_out". C++ signature :  bool punch_out_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def re_enable_automation(self, arg1):
            """
            Discards overrides of automated parameters. C++ signature :  void re_enable_automation(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def re_enable_automation_enabled_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "re_enable_automation_enabled". C++ signature :  bool re_enable_automation_enabled_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def record_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "record_mode". C++ signature :  bool record_mode_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def redo(self, arg1):
            """
            Redo the last action that was undone. C++ signature :  void redo(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def remove_appointed_device_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "appointed_device". C++ signature :  void remove_appointed_device_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_arrangement_overdub_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "arrangement_overdub". C++ signature :  void remove_arrangement_overdub_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_back_to_arranger_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "back_to_arranger". C++ signature :  void remove_back_to_arranger_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_can_capture_midi_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "can_capture_midi". C++ signature :  void remove_can_capture_midi_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_can_jump_to_next_cue_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "can_jump_to_next_cue". C++ signature :  void remove_can_jump_to_next_cue_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_can_jump_to_prev_cue_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "can_jump_to_prev_cue". C++ signature :  void remove_can_jump_to_prev_cue_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_clip_trigger_quantization_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "clip_trigger_quantization". C++ signature :  void remove_clip_trigger_quantization_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_count_in_duration_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "count_in_duration". C++ signature :  void remove_count_in_duration_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_cue_points_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "cue_points". C++ signature :  void remove_cue_points_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_current_song_time_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "current_song_time". C++ signature :  void remove_current_song_time_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_data_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "data". C++ signature :  void remove_data_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_exclusive_arm_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "exclusive_arm". C++ signature :  void remove_exclusive_arm_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_groove_amount_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "groove_amount". C++ signature :  void remove_groove_amount_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_counting_in_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_counting_in". C++ signature :  void remove_is_counting_in_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_playing_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_playing". C++ signature :  void remove_is_playing_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_loop_length_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "loop_length". C++ signature :  void remove_loop_length_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_loop_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "loop". C++ signature :  void remove_loop_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_loop_start_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "loop_start". C++ signature :  void remove_loop_start_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_metronome_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "metronome". C++ signature :  void remove_metronome_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_midi_recording_quantization_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "midi_recording_quantization". C++ signature :  void remove_midi_recording_quantization_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_nudge_down_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "nudge_down". C++ signature :  void remove_nudge_down_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_nudge_up_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "nudge_up". C++ signature :  void remove_nudge_up_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_overdub_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "overdub". C++ signature :  void remove_overdub_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_punch_in_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "punch_in". C++ signature :  void remove_punch_in_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_punch_out_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "punch_out". C++ signature :  void remove_punch_out_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_re_enable_automation_enabled_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "re_enable_automation_enabled". C++ signature :  void remove_re_enable_automation_enabled_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_record_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "record_mode". C++ signature :  void remove_record_mode_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_return_tracks_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "return_tracks". C++ signature :  void remove_return_tracks_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_root_note_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "root_note". C++ signature :  void remove_root_note_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_scale_intervals_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "scale_intervals". C++ signature :  void remove_scale_intervals_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_scale_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "scale_name". C++ signature :  void remove_scale_name_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_scenes_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "scenes". C++ signature :  void remove_scenes_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_session_automation_record_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "session_automation_record". C++ signature :  void remove_session_automation_record_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_session_record_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "session_record". C++ signature :  void remove_session_record_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_session_record_status_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "session_record_status". C++ signature :  void remove_session_record_status_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_signature_denominator_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "signature_denominator". C++ signature :  void remove_signature_denominator_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_signature_numerator_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "signature_numerator". C++ signature :  void remove_signature_numerator_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_song_length_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "song_length". C++ signature :  void remove_song_length_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_swing_amount_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "swing_amount". C++ signature :  void remove_swing_amount_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_tempo_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "tempo". C++ signature :  void remove_tempo_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_tracks_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "tracks". C++ signature :  void remove_tracks_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_visible_tracks_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "visible_tracks". C++ signature :  void remove_visible_tracks_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def return_tracks_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "return_tracks". C++ signature :  bool return_tracks_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def root_note_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "root_note". C++ signature :  bool root_note_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def scale_intervals_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "scale_intervals". C++ signature :  bool scale_intervals_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def scale_name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "scale_name". C++ signature :  bool scale_name_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def scenes_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "scenes". C++ signature :  bool scenes_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def scrub_by(self, arg1, arg2):
            """
            Same as jump_by, but does not stop playback. C++ signature :  void scrub_by(TPyHandle<ASong>,double)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: float
            """
            pass

        def session_automation_record_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "session_automation_record". C++ signature :  bool session_automation_record_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def session_record_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "session_record". C++ signature :  bool session_record_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def session_record_status_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "session_record_status". C++ signature :  bool session_record_status_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def set_data(self, arg1, key, value):
            """
            Store data for the given key in this object. The data is persistent and will be restored when loading the Live Set. C++ signature :  void set_data(TPyHandle<ASong>,TString,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param key: key
            :type key: object
            :param value: value
            :type value: object
            """
            pass

        def set_or_delete_cue(self, arg1):
            """
            When a cue is selected, it gets deleted. If no cue is selected, a new cue is created at the current global songtime. C++ signature :  void set_or_delete_cue(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def signature_denominator_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "signature_denominator". C++ signature :  bool signature_denominator_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def signature_numerator_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "signature_numerator". C++ signature :  bool signature_numerator_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def song_length_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "song_length". C++ signature :  bool song_length_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def start_playing(self, arg1):
            """
            Start playing from the startmarker C++ signature :  void start_playing(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def stop_all_clips(self, arg1, Quantized=True):
            """
            Stop all playing Clips (if any) but continue playing the Song. C++ signature :  void stop_all_clips(TPyHandle<ASong> [,bool=True])
            :param arg1: arg1
            :type arg1: Song
            :param Quantized: Quantized defaults to True 
            :type Quantized: bool
            """
            pass

        def stop_playing(self, arg1):
            """
            Stop playing the Song. C++ signature :  void stop_playing(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def swing_amount_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "swing_amount". C++ signature :  bool swing_amount_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def tap_tempo(self, arg1):
            """
            Trigger the tap tempo function. C++ signature :  void tap_tempo(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def tempo_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "tempo". C++ signature :  bool tempo_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def tracks_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "tracks". C++ signature :  bool tracks_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def trigger_session_record(self, handle, record_length=1.7976931348623157e+308):
            """
            Triggers a new session recording. C++ signature :  void trigger_session_record(TPyHandle<ASong> [,double=1.7976931348623157e+308])
            :param handle: handle
            :type handle: Song
            :param record_length: record_length defaults to 1.7976931348623157e+308 
            :type record_length: float
            """
            pass

        def undo(self, arg1):
            """
            Undo the last action that was made. C++ signature :  void undo(TPyHandle<ASong>)
            :param arg1: arg1
            :type arg1: Song
            """
            pass

        def visible_tracks_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "visible_tracks". C++ signature :  bool visible_tracks_has_listener(TPyHandle<ASong>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Song
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a Live document: The Session and Arrangerview.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the song view.
                """
                pass

            @property
            def detail_clip(self):
                """
                Get/Set the Clip that is currently visible in Lives Detailview.
                """
                pass

            @property
            def draw_mode(self):
                """
                Get/Set if the Envelope/Note draw mode is enabled.
                """
                pass

            @property
            def follow_song(self):
                """
                Get/Set if the Arrangerview should scroll to show the playmarker.
                """
                pass

            @property
            def highlighted_clip_slot(self):
                """
                Get/Set the clip slot, defined via the highlighted track and scene in the Session.Will be None for Master- and Sendtracks.
                """
                pass

            @property
            def selected_chain(self):
                """
                Get the highlighted chain if available.
                """
                pass

            @property
            def selected_parameter(self):
                """
                Get the currently selected device parameter.
                """
                pass

            @property
            def selected_scene(self):
                """
                Get/Set the current selected scene in Lives Sessionview.
                """
                pass

            @property
            def selected_track(self):
                """
                Get/Set the current selected Track in Lives Session or Arrangerview.
                """
                pass

            def add_detail_clip_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "detail_clip" has changed. C++ signature :  void add_detail_clip_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_draw_mode_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "draw_mode" has changed. C++ signature :  void add_draw_mode_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_follow_song_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "follow_song" has changed. C++ signature :  void add_follow_song_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_selected_chain_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "selected_chain" has changed. C++ signature :  void add_selected_chain_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_selected_parameter_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "selected_parameter" has changed. C++ signature :  void add_selected_parameter_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_selected_scene_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "selected_scene" has changed. C++ signature :  void add_selected_scene_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_selected_track_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "selected_track" has changed. C++ signature :  void add_selected_track_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def detail_clip_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "detail_clip". C++ signature :  bool detail_clip_has_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def draw_mode_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "draw_mode". C++ signature :  bool draw_mode_has_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def follow_song_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "follow_song". C++ signature :  bool follow_song_has_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_detail_clip_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "detail_clip". C++ signature :  void remove_detail_clip_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_draw_mode_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "draw_mode". C++ signature :  void remove_draw_mode_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_follow_song_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "follow_song". C++ signature :  void remove_follow_song_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_selected_chain_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "selected_chain". C++ signature :  void remove_selected_chain_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_selected_parameter_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "selected_parameter". C++ signature :  void remove_selected_parameter_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_selected_scene_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "selected_scene". C++ signature :  void remove_selected_scene_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_selected_track_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "selected_track". C++ signature :  void remove_selected_track_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def select_device(self, arg1, arg2, ShouldAppointDevice=True):
                """
                Select the given device. C++ signature :  void select_device(TPyViewData<ASong>,TPyHandle<ADevice> [,bool=True])
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: Device
                :param ShouldAppointDevice: ShouldAppointDevice defaults to True 
                :type ShouldAppointDevice: bool
                """
                pass

            def selected_chain_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "selected_chain". C++ signature :  bool selected_chain_has_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def selected_parameter_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "selected_parameter". C++ signature :  bool selected_parameter_has_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def selected_scene_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "selected_scene". C++ signature :  bool selected_scene_has_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def selected_track_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "selected_track". C++ signature :  bool selected_track_has_listener(TPyViewData<ASong>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

    class TimeFormat(object):
        def __init__(self, *a, *k):
            pass

        @property
        def ms_time(self):
            pass

        @property
        def smpte_24(self):
            pass

        @property
        def smpte_25(self):
            pass

        @property
        def smpte_29(self):
            pass

        @property
        def smpte_30(self):
            pass

        @property
        def smpte_30_drop(self):
            pass


class Track(ModuleType):
    pass

    class DeviceContainer(object):
        def __init__(self, *a, *k):
            """
            This class is a common super class of Track and Chain
            """
            pass

        @property
        def _live_ptr(self):
            pass

    class DeviceInsertMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def count(self):
            pass

        @property
        def default(self):
            pass

        @property
        def selected_left(self):
            pass

        @property
        def selected_right(self):
            pass

    class RoutingChannel(object):
        def __init__(self, *a, *k):
            """
            This class represents a routing channel.
            """
            pass

        @property
        def display_name(self):
            """
            Display name of routing channel.
            """
            pass

        @property
        def layout(self):
            """
            The routing channel's Layout, e.g., mono or stereo.
            """
            pass

    class RoutingChannelLayout(object):
        def __init__(self, *a, *k):
            pass

        @property
        def midi(self):
            pass

        @property
        def mono(self):
            pass

        @property
        def stereo(self):
            pass

    class RoutingChannelVector(object):
        def __init__(self, *a, *k):
            """
            A container for returning routing channels from Live.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<NRoutingApi::TRoutingChannel, std::__1::allocator<NRoutingApi::TRoutingChannel> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: RoutingChannelVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<NRoutingApi::TRoutingChannel, std::__1::allocator<NRoutingApi::TRoutingChannel> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: RoutingChannelVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

    class RoutingType(object):
        def __init__(self, *a, *k):
            """
            This class represents a routing type.
            """
            pass

        @property
        def attached_object(self):
            """
            Live object associated with the routing type.
            """
            pass

        @property
        def category(self):
            """
            Category of the routing type.
            """
            pass

        @property
        def display_name(self):
            """
            Display name of routing type.
            """
            pass

    class RoutingTypeCategory(object):
        def __init__(self, *a, *k):
            pass

        @property
        def external(self):
            pass

        @property
        def invalid(self):
            pass

        @property
        def master(self):
            pass

        @property
        def none(self):
            pass

        @property
        def parent_group_track(self):
            pass

        @property
        def resampling(self):
            pass

        @property
        def rewire(self):
            pass

        @property
        def track(self):
            pass

    class RoutingTypeVector(object):
        def __init__(self, *a, *k):
            """
            A container for returning routing types from Live.
            """
            pass

        def append(self, arg1, arg2):
            """
            C++ signature :  void append(std::__1::vector<NRoutingApi::TRoutingType, std::__1::allocator<NRoutingApi::TRoutingType> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: RoutingTypeVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def extend(self, arg1, arg2):
            """
            C++ signature :  void extend(std::__1::vector<NRoutingApi::TRoutingType, std::__1::allocator<NRoutingApi::TRoutingType> > {lvalue},boost::python::api::object)
            :param arg1: arg1
            :type arg1: RoutingTypeVector
            :param arg2: arg2
            :type arg2: object
            """
            pass

    class Track(object):
        def __init__(self, *a, *k):
            """
            This class represents a track in Live. It can be either an Audio track, a MIDI Track, a Return Track or the Master track. The Master Track and at least one Audio or MIDI track will be always present.Return Tracks are optional.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def arm(self):
            """
            Arm the track for recording. Not available for Master- and Send Tracks.
            """
            pass

        @property
        def arrangement_clips(self):
            """
            const access to the list of clips in arrangement viewThe list will be empty for the master, send and group tracks.
            """
            pass

        @property
        def available_input_routing_channels(self):
            """
            Return a list of source channels for input routing.
            """
            pass

        @property
        def available_input_routing_types(self):
            """
            Return a list of source types for input routing.
            """
            pass

        @property
        def available_output_routing_channels(self):
            """
            Return a list of destination channels for output routing.
            """
            pass

        @property
        def available_output_routing_types(self):
            """
            Return a list of destination types for output routing.
            """
            pass

        @property
        def can_be_armed(self):
            """
            return True, if this Track has a valid arm property. Not all trackscan be armed (for example return Tracks or the Master Tracks).
            """
            pass

        @property
        def can_be_frozen(self):
            """
            return True, if this Track can be frozen.
            """
            pass

        @property
        def can_show_chains(self):
            """
            return True, if this Track contains a rack instrument device that is capable of showing its chains in session view.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the track.
            """
            pass

        @property
        def clip_slots(self):
            """
            const access to the list of clipslots (see class AClipSlot) for this track.The list will be empty for the master and sendtracks.
            """
            pass

        @property
        def color(self):
            """
            Get/set access to the color of the Track (RGB).
            """
            pass

        @property
        def color_index(self):
            """
            Get/Set access to the color index of the track. Can be None for no color.
            """
            pass

        @property
        def current_input_routing(self):
            """
            Get/Set the name of the current active input routing.When setting a new routing, the new routing must be one of the available ones.
            """
            pass

        @property
        def current_input_sub_routing(self):
            """
            Get/Set the current active input sub routing.When setting a new routing, the new routing must be one of the available ones.
            """
            pass

        @property
        def current_monitoring_state(self):
            """
            Get/Set the track's current monitoring state.
            """
            pass

        @property
        def current_output_routing(self):
            """
            Get/Set the current active output routing.When setting a new routing, the new routing must be one of the available ones.
            """
            pass

        @property
        def current_output_sub_routing(self):
            """
            Get/Set the current active output sub routing.When setting a new routing, the new routing must be one of the available ones.
            """
            pass

        @property
        def devices(self):
            """
            Return const access to all available Devices that are present in the TracksDevicechain. This tuple will also include the 'mixer_device' that every Trackalways has.
            """
            pass

        @property
        def fired_slot_index(self):
            """
            const access to the index of the fired (and thus blinking) clipslot in this track.This index is -1 if no slot is fired and -2 if the track's stop button has been fired.
            """
            pass

        @property
        def fold_state(self):
            """
            Get/Set whether the track is folded or not. Only available if is_foldable is True.
            """
            pass

        @property
        def group_track(self):
            """
            return the group track if is_grouped.
            """
            pass

        @property
        def has_audio_input(self):
            """
            return True, if this Track can be feed with an Audio signal. This istrue for all Audio Tracks.
            """
            pass

        @property
        def has_audio_output(self):
            """
            return True, if this Track sends out an Audio signal. This istrue for all Audio Tracks, and MIDI tracks with an Instrument.
            """
            pass

        @property
        def has_midi_input(self):
            """
            return True, if this Track can be feed with an Audio signal. This istrue for all MIDI Tracks.
            """
            pass

        @property
        def has_midi_output(self):
            """
            return True, if this Track sends out MIDI events. This istrue for all MIDI Tracks with no Instruments.
            """
            pass

        @property
        def implicit_arm(self):
            """
            Arm the track for recording. When The track is implicitly armed, it showsin a weaker color in the live GUI and is not saved in the set.
            """
            pass

        @property
        def input_meter_left(self):
            """
            Momentary value of left input channel meter, 0.0 to 1.0. For Audio Tracks only.
            """
            pass

        @property
        def input_meter_level(self):
            """
            Return the MIDI or Audio meter value of the Tracks input, depending on thetype of the Track input. Meter values (MIDI or Audio) are always scaledfrom 0.0 to 1.0.
            """
            pass

        @property
        def input_meter_right(self):
            """
            Momentary value of right input channel meter, 0.0 to 1.0. For Audio Tracks only.
            """
            pass

        @property
        def input_routing_channel(self):
            """
            Get and set the current source channel for input routing.Raises ValueError if the type isn't one of the current values inavailable_input_routing_channels.
            """
            pass

        @property
        def input_routing_type(self):
            """
            Get and set the current source type for input routing.Raises ValueError if the type isn't one of the current values inavailable_input_routing_types.
            """
            pass

        @property
        def input_routings(self):
            """
            Const access to the list of available input routings.
            """
            pass

        @property
        def input_sub_routings(self):
            """
            Return a list of all available input sub routings.
            """
            pass

        @property
        def is_foldable(self):
            """
            return True if the track can be (un)folded to hide/reveal contained tracks.
            """
            pass

        @property
        def is_frozen(self):
            """
            return True if this Track is currently frozen. No changes should be applied to the track's devices or clips while it is frozen.
            """
            pass

        @property
        def is_grouped(self):
            """
            return True if this Track is current part of a group track.
            """
            pass

        @property
        def is_part_of_selection(self):
            """
            return False if the track is not selected.
            """
            pass

        @property
        def is_showing_chains(self):
            """
            Get/Set whether a track with a rack device is showing its chains in session view.
            """
            pass

        @property
        def is_visible(self):
            """
            return False if the track is hidden within a folded group track.
            """
            pass

        @property
        def mixer_device(self):
            """
            Return access to the special Device that every Track has: This Device containsthe Volume, Pan, Sendamounts, and Crossfade assignment parameters.
            """
            pass

        @property
        def mute(self):
            """
            Mute/unmute the track.
            """
            pass

        @property
        def muted_via_solo(self):
            """
            Returns true if the track is muted because another track is soloed.
            """
            pass

        @property
        def name(self):
            """
            Read/write access to the name of the Track, as visible in the track header.
            """
            pass

        @property
        def output_meter_left(self):
            """
            Momentary value of left output channel meter, 0.0 to 1.0.For tracks with audio output only.
            """
            pass

        @property
        def output_meter_level(self):
            """
            Return the MIDI or Audio meter value of the Track output (behind themixer_device), depending on the type of the Track input, this can be a MIDIor Audio meter. Meter values (MIDI or Audio) are always scaled from 0.0 to 1.0.
            """
            pass

        @property
        def output_meter_right(self):
            """
            Momentary value of right output channel meter, 0.0 to 1.0.For tracks with audio output only.
            """
            pass

        @property
        def output_routing_channel(self):
            """
            Get and set the current destination channel for output routing.Raises ValueError if the channel isn't one of the current values inavailable_output_routing_channels.
            """
            pass

        @property
        def output_routing_type(self):
            """
            Get and set the current destination type for output routing.Raises ValueError if the type isn't one of the current values inavailable_output_routing_types.
            """
            pass

        @property
        def output_routings(self):
            """
            Const access to the list of all available output routings.
            """
            pass

        @property
        def output_sub_routings(self):
            """
            Return a list of all available output sub routings.
            """
            pass

        @property
        def playing_slot_index(self):
            """
            const access to the index of the currently playing clip in the track.Will be -1 when no clip is playing.
            """
            pass

        @property
        def solo(self):
            """
            Get/Set the solo status of the track. Note that this will not disable thesolo state of any other track. If you want exclusive solo, you have to disable the solo state of the other Tracks manually.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a Track.
            """
            pass

        def add_arm_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "arm" has changed. C++ signature :  void add_arm_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_arrangement_clips_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "arrangement_clips" has changed. C++ signature :  void add_arrangement_clips_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_available_input_routing_channels_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "available_input_routing_channels" has changed. C++ signature :  void add_available_input_routing_channels_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_available_input_routing_types_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "available_input_routing_types" has changed. C++ signature :  void add_available_input_routing_types_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_available_output_routing_channels_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "available_output_routing_channels" has changed. C++ signature :  void add_available_output_routing_channels_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_available_output_routing_types_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "available_output_routing_types" has changed. C++ signature :  void add_available_output_routing_types_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_clip_slots_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "clip_slots" has changed. C++ signature :  void add_clip_slots_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_color_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color_index" has changed. C++ signature :  void add_color_index_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_color_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "color" has changed. C++ signature :  void add_color_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_current_input_routing_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "current_input_routing" has changed. C++ signature :  void add_current_input_routing_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_current_input_sub_routing_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "current_input_sub_routing" has changed. C++ signature :  void add_current_input_sub_routing_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_current_monitoring_state_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "current_monitoring_state" has changed. C++ signature :  void add_current_monitoring_state_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_current_output_routing_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "current_output_routing" has changed. C++ signature :  void add_current_output_routing_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_current_output_sub_routing_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "current_output_sub_routing" has changed. C++ signature :  void add_current_output_sub_routing_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_data_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "data" has changed. C++ signature :  void add_data_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_devices_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "devices" has changed. C++ signature :  void add_devices_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_fired_slot_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "fired_slot_index" has changed. C++ signature :  void add_fired_slot_index_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_has_audio_input_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "has_audio_input" has changed. C++ signature :  void add_has_audio_input_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_has_audio_output_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "has_audio_output" has changed. C++ signature :  void add_has_audio_output_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_has_midi_input_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "has_midi_input" has changed. C++ signature :  void add_has_midi_input_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_has_midi_output_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "has_midi_output" has changed. C++ signature :  void add_has_midi_output_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_implicit_arm_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "implicit_arm" has changed. C++ signature :  void add_implicit_arm_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_input_meter_left_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "input_meter_left" has changed. C++ signature :  void add_input_meter_left_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_input_meter_level_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "input_meter_level" has changed. C++ signature :  void add_input_meter_level_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_input_meter_right_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "input_meter_right" has changed. C++ signature :  void add_input_meter_right_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_input_routing_channel_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "input_routing_channel" has changed. C++ signature :  void add_input_routing_channel_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_input_routing_type_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "input_routing_type" has changed. C++ signature :  void add_input_routing_type_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_input_routings_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "input_routings" has changed. C++ signature :  void add_input_routings_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_input_sub_routings_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "input_sub_routings" has changed. C++ signature :  void add_input_sub_routings_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_frozen_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_frozen" has changed. C++ signature :  void add_is_frozen_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_showing_chains_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_showing_chains" has changed. C++ signature :  void add_is_showing_chains_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_mute_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "mute" has changed. C++ signature :  void add_mute_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_muted_via_solo_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "muted_via_solo" has changed. C++ signature :  void add_muted_via_solo_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_output_meter_left_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "output_meter_left" has changed. C++ signature :  void add_output_meter_left_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_output_meter_level_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "output_meter_level" has changed. C++ signature :  void add_output_meter_level_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_output_meter_right_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "output_meter_right" has changed. C++ signature :  void add_output_meter_right_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_output_routing_channel_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "output_routing_channel" has changed. C++ signature :  void add_output_routing_channel_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_output_routing_type_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "output_routing_type" has changed. C++ signature :  void add_output_routing_type_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_output_routings_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "output_routings" has changed. C++ signature :  void add_output_routings_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_output_sub_routings_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "output_sub_routings" has changed. C++ signature :  void add_output_sub_routings_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_playing_slot_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "playing_slot_index" has changed. C++ signature :  void add_playing_slot_index_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_solo_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "solo" has changed. C++ signature :  void add_solo_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def arm_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "arm". C++ signature :  bool arm_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def arrangement_clips_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "arrangement_clips". C++ signature :  bool arrangement_clips_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def available_input_routing_channels_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "available_input_routing_channels". C++ signature :  bool available_input_routing_channels_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def available_input_routing_types_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "available_input_routing_types". C++ signature :  bool available_input_routing_types_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def available_output_routing_channels_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "available_output_routing_channels". C++ signature :  bool available_output_routing_channels_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def available_output_routing_types_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "available_output_routing_types". C++ signature :  bool available_output_routing_types_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def clip_slots_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "clip_slots". C++ signature :  bool clip_slots_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def color_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color". C++ signature :  bool color_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def color_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "color_index". C++ signature :  bool color_index_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def current_input_routing_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "current_input_routing". C++ signature :  bool current_input_routing_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def current_input_sub_routing_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "current_input_sub_routing". C++ signature :  bool current_input_sub_routing_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def current_monitoring_state_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "current_monitoring_state". C++ signature :  bool current_monitoring_state_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def current_output_routing_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "current_output_routing". C++ signature :  bool current_output_routing_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def current_output_sub_routing_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "current_output_sub_routing". C++ signature :  bool current_output_sub_routing_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def data_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "data". C++ signature :  bool data_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def delete_clip(self, arg1, arg2):
            """
            Delete the given clip. Raises a runtime error when the clip belongs to another track. C++ signature :  void delete_clip(TTrackPyHandle,TPyHandle<AClip>)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: Clip
            """
            pass

        def delete_device(self, arg1, arg2):
            """
            Delete a device identified by the index in the 'devices' list. C++ signature :  void delete_device(TTrackPyHandle,int)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: int
            """
            pass

        def devices_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "devices". C++ signature :  bool devices_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def duplicate_clip_slot(self, arg1, arg2):
            """
            Duplicate a clip and put it into the next free slot and return the index of the destination slot. A new scene is created if no free slot is available. If creating the new scene would exceed the limitations, a runtime error is raised. C++ signature :  int duplicate_clip_slot(TTrackPyHandle,int)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: int
            :rtype: int
            """
            pass

        def duplicate_clip_to_arrangement(self, handle, clip, destination_time):
            """
            Duplicate the given clip into the arrangement of this track at the provided destination time and return it. When the type of the clip and the type of the track are incompatible, a runtime error is raised. C++ signature :  TWeakPtr<TPyHandle<AClip> > duplicate_clip_to_arrangement(TTrackPyHandle,TPyHandle<AClip>,double)
            :param handle: handle
            :type handle: Track
            :param clip: clip
            :type clip: Clip
            :param destination_time: destination_time
            :type destination_time: float
            :rtype: Clip
            """
            pass

        def fired_slot_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "fired_slot_index". C++ signature :  bool fired_slot_index_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def get_data(self, arg1, key, default_value):
            """
            Get data for the given key, that was previously stored using set_data. C++ signature :  boost::python::api::object get_data(TTrackPyHandle,TString,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param key: key
            :type key: object
            :param default_value: default_value
            :type default_value: object
            :rtype: object
            """
            pass

        def has_audio_input_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "has_audio_input". C++ signature :  bool has_audio_input_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def has_audio_output_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "has_audio_output". C++ signature :  bool has_audio_output_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def has_midi_input_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "has_midi_input". C++ signature :  bool has_midi_input_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def has_midi_output_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "has_midi_output". C++ signature :  bool has_midi_output_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def implicit_arm_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "implicit_arm". C++ signature :  bool implicit_arm_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def input_meter_left_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "input_meter_left". C++ signature :  bool input_meter_left_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def input_meter_level_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "input_meter_level". C++ signature :  bool input_meter_level_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def input_meter_right_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "input_meter_right". C++ signature :  bool input_meter_right_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def input_routing_channel_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "input_routing_channel". C++ signature :  bool input_routing_channel_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def input_routing_type_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "input_routing_type". C++ signature :  bool input_routing_type_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def input_routings_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "input_routings". C++ signature :  bool input_routings_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def input_sub_routings_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "input_sub_routings". C++ signature :  bool input_sub_routings_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_frozen_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_frozen". C++ signature :  bool is_frozen_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_showing_chains_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_showing_chains". C++ signature :  bool is_showing_chains_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def jump_in_running_session_clip(self, arg1, arg2):
            """
            Jump forward or backward in the currently running Sessionclip (if any) by the specified relative amount in beats. Does nothing if no Session Clip is currently running. C++ signature :  void jump_in_running_session_clip(TTrackPyHandle,double)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: float
            """
            pass

        def mute_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "mute". C++ signature :  bool mute_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def muted_via_solo_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "muted_via_solo". C++ signature :  bool muted_via_solo_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def output_meter_left_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "output_meter_left". C++ signature :  bool output_meter_left_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def output_meter_level_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "output_meter_level". C++ signature :  bool output_meter_level_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def output_meter_right_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "output_meter_right". C++ signature :  bool output_meter_right_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def output_routing_channel_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "output_routing_channel". C++ signature :  bool output_routing_channel_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def output_routing_type_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "output_routing_type". C++ signature :  bool output_routing_type_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def output_routings_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "output_routings". C++ signature :  bool output_routings_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def output_sub_routings_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "output_sub_routings". C++ signature :  bool output_sub_routings_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def playing_slot_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "playing_slot_index". C++ signature :  bool playing_slot_index_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_arm_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "arm". C++ signature :  void remove_arm_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_arrangement_clips_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "arrangement_clips". C++ signature :  void remove_arrangement_clips_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_available_input_routing_channels_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "available_input_routing_channels". C++ signature :  void remove_available_input_routing_channels_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_available_input_routing_types_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "available_input_routing_types". C++ signature :  void remove_available_input_routing_types_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_available_output_routing_channels_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "available_output_routing_channels". C++ signature :  void remove_available_output_routing_channels_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_available_output_routing_types_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "available_output_routing_types". C++ signature :  void remove_available_output_routing_types_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_clip_slots_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "clip_slots". C++ signature :  void remove_clip_slots_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_color_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color_index". C++ signature :  void remove_color_index_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_color_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "color". C++ signature :  void remove_color_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_current_input_routing_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "current_input_routing". C++ signature :  void remove_current_input_routing_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_current_input_sub_routing_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "current_input_sub_routing". C++ signature :  void remove_current_input_sub_routing_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_current_monitoring_state_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "current_monitoring_state". C++ signature :  void remove_current_monitoring_state_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_current_output_routing_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "current_output_routing". C++ signature :  void remove_current_output_routing_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_current_output_sub_routing_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "current_output_sub_routing". C++ signature :  void remove_current_output_sub_routing_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_data_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "data". C++ signature :  void remove_data_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_devices_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "devices". C++ signature :  void remove_devices_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_fired_slot_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "fired_slot_index". C++ signature :  void remove_fired_slot_index_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_has_audio_input_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "has_audio_input". C++ signature :  void remove_has_audio_input_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_has_audio_output_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "has_audio_output". C++ signature :  void remove_has_audio_output_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_has_midi_input_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "has_midi_input". C++ signature :  void remove_has_midi_input_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_has_midi_output_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "has_midi_output". C++ signature :  void remove_has_midi_output_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_implicit_arm_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "implicit_arm". C++ signature :  void remove_implicit_arm_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_input_meter_left_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "input_meter_left". C++ signature :  void remove_input_meter_left_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_input_meter_level_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "input_meter_level". C++ signature :  void remove_input_meter_level_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_input_meter_right_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "input_meter_right". C++ signature :  void remove_input_meter_right_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_input_routing_channel_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "input_routing_channel". C++ signature :  void remove_input_routing_channel_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_input_routing_type_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "input_routing_type". C++ signature :  void remove_input_routing_type_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_input_routings_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "input_routings". C++ signature :  void remove_input_routings_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_input_sub_routings_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "input_sub_routings". C++ signature :  void remove_input_sub_routings_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_frozen_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_frozen". C++ signature :  void remove_is_frozen_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_showing_chains_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_showing_chains". C++ signature :  void remove_is_showing_chains_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_mute_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "mute". C++ signature :  void remove_mute_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_muted_via_solo_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "muted_via_solo". C++ signature :  void remove_muted_via_solo_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_output_meter_left_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "output_meter_left". C++ signature :  void remove_output_meter_left_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_output_meter_level_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "output_meter_level". C++ signature :  void remove_output_meter_level_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_output_meter_right_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "output_meter_right". C++ signature :  void remove_output_meter_right_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_output_routing_channel_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "output_routing_channel". C++ signature :  void remove_output_routing_channel_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_output_routing_type_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "output_routing_type". C++ signature :  void remove_output_routing_type_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_output_routings_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "output_routings". C++ signature :  void remove_output_routings_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_output_sub_routings_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "output_sub_routings". C++ signature :  void remove_output_sub_routings_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_playing_slot_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "playing_slot_index". C++ signature :  void remove_playing_slot_index_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_solo_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "solo". C++ signature :  void remove_solo_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def set_data(self, arg1, key, value):
            """
            Store data for the given key in this object. The data is persistent and will be restored when loading the Live Set. C++ signature :  void set_data(TTrackPyHandle,TString,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param key: key
            :type key: object
            :param value: value
            :type value: object
            """
            pass

        def solo_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "solo". C++ signature :  bool solo_has_listener(TTrackPyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Track
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def stop_all_clips(self, arg1, Quantized=True):
            """
            Stop running and triggered clip and slots on this track. C++ signature :  void stop_all_clips(TTrackPyHandle [,bool=True])
            :param arg1: arg1
            :type arg1: Track
            :param Quantized: Quantized defaults to True 
            :type Quantized: bool
            """
            pass

        class monitoring_states(object):
            def __init__(self, *a, *k):
                pass

            @property
            def AUTO(self):
                pass

            @property
            def IN(self):
                pass

            @property
            def OFF(self):
                pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a Track.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the track view.
                """
                pass

            @property
            def device_insert_mode(self):
                """
                Get/Listen the device insertion mode of the track.  By default, it will insert devices at the end, but it can be changed to make it relative to current selection.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the track is shown collapsed in the arranger view.
                """
                pass

            @property
            def selected_device(self):
                """
                Get/Set/Listen the insertion mode of the device.  While in insertion mode, loading new devices from the browser will place devices at the selected position.
                """
                pass

            def add_device_insert_mode_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "device_insert_mode" has changed. C++ signature :  void add_device_insert_mode_listener(TPyViewData<ATrack>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ATrack>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def add_selected_device_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "selected_device" has changed. C++ signature :  void add_selected_device_listener(TPyViewData<ATrack>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def device_insert_mode_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "device_insert_mode". C++ signature :  bool device_insert_mode_has_listener(TPyViewData<ATrack>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ATrack>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_device_insert_mode_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "device_insert_mode". C++ signature :  void remove_device_insert_mode_listener(TPyViewData<ATrack>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ATrack>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def remove_selected_device_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "selected_device". C++ signature :  void remove_selected_device_listener(TPyViewData<ATrack>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def select_instrument(self, arg1):
                """
                Selects the track's instrument if it has one. C++ signature :  bool select_instrument(TPyViewData<ATrack>)
                :param arg1: arg1
                :type arg1: View
                :rtype: bool
                """
                pass

            def selected_device_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "selected_device". C++ signature :  bool selected_device_has_listener(TPyViewData<ATrack>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass


class TransmuteDevice(ModuleType):
    pass

    class TransmuteDevice(object):
        def __init__(self, *a, *k):
            """
            This class represents a Transmute device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def can_have_chains(self):
            """
            Returns true if the device is a rack.
            """
            pass

        @property
        def can_have_drum_pads(self):
            """
            Returns true if the device is a drum rack.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Device.
            """
            pass

        @property
        def class_display_name(self):
            """
            Return const access to the name of the device's class name as displayed in Live's browser and device chain
            """
            pass

        @property
        def class_name(self):
            """
            Return const access to the name of the device's class.
            """
            pass

        @property
        def frequency_dial_mode_index(self):
            """
            Return the current frequency dial mode index
            """
            pass

        @property
        def frequency_dial_mode_list(self):
            """
            Return the current frequency dial mode list
            """
            pass

        @property
        def is_active(self):
            """
            Return const access to whether this device is active. This will be false bothwhen the device is off and when it's inside a rack device which is off.
            """
            pass

        @property
        def midi_gate_index(self):
            """
            Return the current midi gate index
            """
            pass

        @property
        def midi_gate_list(self):
            """
            Return the current midi gate list
            """
            pass

        @property
        def mod_mode_index(self):
            """
            Return the current mod mode index
            """
            pass

        @property
        def mod_mode_list(self):
            """
            Return the current mod mode list
            """
            pass

        @property
        def mono_poly_index(self):
            """
            Return the current mono poly mode index
            """
            pass

        @property
        def mono_poly_list(self):
            """
            Return the current mono poly mode list
            """
            pass

        @property
        def name(self):
            """
            Return access to the name of the device.
            """
            pass

        @property
        def parameters(self):
            """
            Const access to the list of available automatable parameters for this device.
            """
            pass

        @property
        def pitch_bend_range(self):
            """
            Return the current pitch bend range
            """
            pass

        @property
        def pitch_mode_index(self):
            """
            Return the current pitch mode index
            """
            pass

        @property
        def pitch_mode_list(self):
            """
            Return the current pitch mode list
            """
            pass

        @property
        def polyphony(self):
            """
            Return the current polyphony
            """
            pass

        @property
        def type(self):
            """
            Return the type of the device.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a device.
            """
            pass

        def add_frequency_dial_mode_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "frequency_dial_mode_index" has changed. C++ signature :  void add_frequency_dial_mode_index_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_frequency_dial_mode_list_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "frequency_dial_mode_list" has changed. C++ signature :  void add_frequency_dial_mode_list_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_active_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_active" has changed. C++ signature :  void add_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_midi_gate_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "midi_gate_index" has changed. C++ signature :  void add_midi_gate_index_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_midi_gate_list_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "midi_gate_list" has changed. C++ signature :  void add_midi_gate_list_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_mod_mode_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "mod_mode_index" has changed. C++ signature :  void add_mod_mode_index_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_mod_mode_list_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "mod_mode_list" has changed. C++ signature :  void add_mod_mode_list_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_mono_poly_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "mono_poly_index" has changed. C++ signature :  void add_mono_poly_index_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_mono_poly_list_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "mono_poly_list" has changed. C++ signature :  void add_mono_poly_list_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_parameters_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "parameters" has changed. C++ signature :  void add_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_pitch_bend_range_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "pitch_bend_range" has changed. C++ signature :  void add_pitch_bend_range_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_pitch_mode_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "pitch_mode_index" has changed. C++ signature :  void add_pitch_mode_index_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_pitch_mode_list_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "pitch_mode_list" has changed. C++ signature :  void add_pitch_mode_list_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_polyphony_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "polyphony" has changed. C++ signature :  void add_polyphony_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def frequency_dial_mode_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "frequency_dial_mode_index". C++ signature :  bool frequency_dial_mode_index_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def frequency_dial_mode_list_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "frequency_dial_mode_list". C++ signature :  bool frequency_dial_mode_list_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_active_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_active". C++ signature :  bool is_active_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def midi_gate_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "midi_gate_index". C++ signature :  bool midi_gate_index_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def midi_gate_list_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "midi_gate_list". C++ signature :  bool midi_gate_list_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def mod_mode_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "mod_mode_index". C++ signature :  bool mod_mode_index_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def mod_mode_list_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "mod_mode_list". C++ signature :  bool mod_mode_list_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def mono_poly_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "mono_poly_index". C++ signature :  bool mono_poly_index_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def mono_poly_list_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "mono_poly_list". C++ signature :  bool mono_poly_list_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def parameters_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "parameters". C++ signature :  bool parameters_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def pitch_bend_range_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "pitch_bend_range". C++ signature :  bool pitch_bend_range_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def pitch_mode_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "pitch_mode_index". C++ signature :  bool pitch_mode_index_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def pitch_mode_list_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "pitch_mode_list". C++ signature :  bool pitch_mode_list_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def polyphony_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "polyphony". C++ signature :  bool polyphony_has_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_frequency_dial_mode_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "frequency_dial_mode_index". C++ signature :  void remove_frequency_dial_mode_index_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_frequency_dial_mode_list_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "frequency_dial_mode_list". C++ signature :  void remove_frequency_dial_mode_list_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_active_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_active". C++ signature :  void remove_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_midi_gate_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "midi_gate_index". C++ signature :  void remove_midi_gate_index_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_midi_gate_list_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "midi_gate_list". C++ signature :  void remove_midi_gate_list_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_mod_mode_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "mod_mode_index". C++ signature :  void remove_mod_mode_index_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_mod_mode_list_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "mod_mode_list". C++ signature :  void remove_mod_mode_list_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_mono_poly_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "mono_poly_index". C++ signature :  void remove_mono_poly_index_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_mono_poly_list_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "mono_poly_list". C++ signature :  void remove_mono_poly_list_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_parameters_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "parameters". C++ signature :  void remove_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_pitch_bend_range_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "pitch_bend_range". C++ signature :  void remove_pitch_bend_range_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_pitch_mode_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "pitch_mode_index". C++ signature :  void remove_pitch_mode_index_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_pitch_mode_list_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "pitch_mode_list". C++ signature :  void remove_pitch_mode_list_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_polyphony_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "polyphony". C++ signature :  void remove_polyphony_listener(TTransmuteDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: TransmuteDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def store_chosen_bank(self, arg1, arg2, arg3):
            """
            Set the selected bank in the device for persistency. C++ signature :  void store_chosen_bank(TPyHandle<ADevice>,int,int)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a device.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the View.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the device is shown collapsed in the device chain.
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass


class WavetableDevice(ModuleType):
    pass

    class EffectMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def frequency_modulation(self):
            pass

        @property
        def none(self):
            pass

        @property
        def sync_and_pulse_width(self):
            pass

        @property
        def warp_and_fold(self):
            pass

    class FilterRouting(object):
        def __init__(self, *a, *k):
            pass

        @property
        def parallel(self):
            pass

        @property
        def serial(self):
            pass

        @property
        def split(self):
            pass

    class ModulationSource(object):
        def __init__(self, *a, *k):
            pass

        @property
        def amp_envelope(self):
            pass

        @property
        def envelope_2(self):
            pass

        @property
        def envelope_3(self):
            pass

        @property
        def lfo_1(self):
            pass

        @property
        def lfo_2(self):
            pass

        @property
        def midi_channel_pressure(self):
            pass

        @property
        def midi_mod_wheel(self):
            pass

        @property
        def midi_note(self):
            pass

        @property
        def midi_pitch_bend(self):
            pass

        @property
        def midi_random(self):
            pass

        @property
        def midi_velocity(self):
            pass

    class UnisonMode(object):
        def __init__(self, *a, *k):
            pass

        @property
        def classic(self):
            pass

        @property
        def fast_shimmer(self):
            pass

        @property
        def none(self):
            pass

        @property
        def phase_sync(self):
            pass

        @property
        def position_spread(self):
            pass

        @property
        def random_note(self):
            pass

        @property
        def slow_shimmer(self):
            pass

    class VoiceCount(object):
        def __init__(self, *a, *k):
            pass

        @property
        def eight(self):
            pass

        @property
        def five(self):
            pass

        @property
        def four(self):
            pass

        @property
        def seven(self):
            pass

        @property
        def six(self):
            pass

        @property
        def three(self):
            pass

        @property
        def two(self):
            pass

    class Voicing(object):
        def __init__(self, *a, *k):
            pass

        @property
        def mono(self):
            pass

        @property
        def poly(self):
            pass

    class WavetableDevice(object):
        def __init__(self, *a, *k):
            """
            This class represents a Wavetable device.
            """
            pass

        @property
        def _live_ptr(self):
            pass

        @property
        def can_have_chains(self):
            """
            Returns true if the device is a rack.
            """
            pass

        @property
        def can_have_drum_pads(self):
            """
            Returns true if the device is a drum rack.
            """
            pass

        @property
        def canonical_parent(self):
            """
            Get the canonical parent of the Device.
            """
            pass

        @property
        def class_display_name(self):
            """
            Return const access to the name of the device's class name as displayed in Live's browser and device chain
            """
            pass

        @property
        def class_name(self):
            """
            Return const access to the name of the device's class.
            """
            pass

        @property
        def filter_routing(self):
            """
            Return the current filter routing.
            """
            pass

        @property
        def is_active(self):
            """
            Return const access to whether this device is active. This will be false bothwhen the device is off and when it's inside a rack device which is off.
            """
            pass

        @property
        def mono_poly(self):
            """
            Return the current voicing mode.
            """
            pass

        @property
        def name(self):
            """
            Return access to the name of the device.
            """
            pass

        @property
        def oscillator_1_effect_mode(self):
            """
            Return the current effect mode of the oscillator 1.
            """
            pass

        @property
        def oscillator_1_wavetable_category(self):
            """
            Return the current wavetable category of the oscillator 1.
            """
            pass

        @property
        def oscillator_1_wavetable_index(self):
            """
            Return the current wavetable index of the oscillator 1.
            """
            pass

        @property
        def oscillator_1_wavetables(self):
            """
            Get a vector of oscillator 1's wavetable names.
            """
            pass

        @property
        def oscillator_2_effect_mode(self):
            """
            Return the current effect mode of the oscillator 2.
            """
            pass

        @property
        def oscillator_2_wavetable_category(self):
            """
            Return the current wavetable category of the oscillator 2.
            """
            pass

        @property
        def oscillator_2_wavetable_index(self):
            """
            Return the current wavetable index of the oscillator 2.
            """
            pass

        @property
        def oscillator_2_wavetables(self):
            """
            Get a vector of oscillator 2's wavetable names.
            """
            pass

        @property
        def oscillator_wavetable_categories(self):
            """
            Get a vector of the available wavetable categories.
            """
            pass

        @property
        def parameters(self):
            """
            Const access to the list of available automatable parameters for this device.
            """
            pass

        @property
        def poly_voices(self):
            """
            Return the current number of polyphonic voices. Uses the VoiceCount enumeration.
            """
            pass

        @property
        def type(self):
            """
            Return the type of the device.
            """
            pass

        @property
        def unison_mode(self):
            """
            Return the current unison mode.
            """
            pass

        @property
        def unison_voice_count(self):
            """
            Return the current number of unison voices.
            """
            pass

        @property
        def view(self):
            """
            Representing the view aspects of a device.
            """
            pass

        @property
        def visible_modulation_target_names(self):
            """
            Get the names of all the visible modulation targets.
            """
            pass

        def add_filter_routing_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "filter_routing" has changed. C++ signature :  void add_filter_routing_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_is_active_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "is_active" has changed. C++ signature :  void add_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_modulation_matrix_changed_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "modulation_matrix_changed" has changed. C++ signature :  void add_modulation_matrix_changed_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_mono_poly_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "mono_poly" has changed. C++ signature :  void add_mono_poly_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_name_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "name" has changed. C++ signature :  void add_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_oscillator_1_effect_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "oscillator_1_effect_mode" has changed. C++ signature :  void add_oscillator_1_effect_mode_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_oscillator_1_wavetable_category_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "oscillator_1_wavetable_category" has changed. C++ signature :  void add_oscillator_1_wavetable_category_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_oscillator_1_wavetable_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "oscillator_1_wavetable_index" has changed. C++ signature :  void add_oscillator_1_wavetable_index_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_oscillator_1_wavetables_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "oscillator_1_wavetables" has changed. C++ signature :  void add_oscillator_1_wavetables_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_oscillator_2_effect_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "oscillator_2_effect_mode" has changed. C++ signature :  void add_oscillator_2_effect_mode_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_oscillator_2_wavetable_category_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "oscillator_2_wavetable_category" has changed. C++ signature :  void add_oscillator_2_wavetable_category_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_oscillator_2_wavetable_index_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "oscillator_2_wavetable_index" has changed. C++ signature :  void add_oscillator_2_wavetable_index_listener(TWavetableDevicePyHandle,boost::python::api::object)add_oscillator_2_wavetable_index_listener( (WavetableDevice)arg1, (object)arg2) -> None : Add a listener function or method, which will be called as soon as the property "oscillator_2_wavetable_index" has changed. C++ signature :  void add_oscillator_2_wavetable_index_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_oscillator_2_wavetables_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "oscillator_2_wavetables" has changed. C++ signature :  void add_oscillator_2_wavetables_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_parameter_to_modulation_matrix(self, handle, parameter):
            """
            Add a non-pitch parameter to the modulation matrix. C++ signature :  int add_parameter_to_modulation_matrix(TWavetableDevicePyHandle,TPyHandle<ATimeableValue>)
            :param handle: handle
            :type handle: WavetableDevice
            :param parameter: parameter
            :type parameter: DeviceParameter
            :rtype: int
            """
            pass

        def add_parameters_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "parameters" has changed. C++ signature :  void add_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_poly_voices_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "poly_voices" has changed. C++ signature :  void add_poly_voices_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_unison_mode_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "unison_mode" has changed. C++ signature :  void add_unison_mode_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_unison_voice_count_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "unison_voice_count" has changed. C++ signature :  void add_unison_voice_count_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def add_visible_modulation_target_names_listener(self, arg1, arg2):
            """
            Add a listener function or method, which will be called as soon as the property "visible_modulation_target_names" has changed. C++ signature :  void add_visible_modulation_target_names_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def filter_routing_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "filter_routing". C++ signature :  bool filter_routing_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def get_modulation_target_parameter_name(self, handle, target_index):
            """
            Get the parameter name of the modulation target at the given index. C++ signature :  TString get_modulation_target_parameter_name(TWavetableDevicePyHandle,int)
            :param handle: handle
            :type handle: WavetableDevice
            :param target_index: target_index
            :type target_index: int
            :rtype: unicode
            """
            pass

        def get_modulation_value(self, handle, target_index, source):
            """
            Get the value of a modulation amount for the given target-source connection. C++ signature :  float get_modulation_value(TWavetableDevicePyHandle,int,int)
            :param handle: handle
            :type handle: WavetableDevice
            :param target_index: target_index
            :type target_index: int
            :param source: source
            :type source: int
            :rtype: float
            """
            pass

        def is_active_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "is_active". C++ signature :  bool is_active_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def is_parameter_modulatable(self, handle, parameter):
            """
            Indicate whether the parameter is modulatable. Note that pitch parameters only exist in python and must be handled there. C++ signature :  bool is_parameter_modulatable(TWavetableDevicePyHandle,TPyHandle<ATimeableValue>)
            :param handle: handle
            :type handle: WavetableDevice
            :param parameter: parameter
            :type parameter: DeviceParameter
            :rtype: bool
            """
            pass

        def modulation_matrix_changed_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "modulation_matrix_changed". C++ signature :  bool modulation_matrix_changed_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def mono_poly_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "mono_poly". C++ signature :  bool mono_poly_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def name_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "name". C++ signature :  bool name_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def oscillator_1_effect_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "oscillator_1_effect_mode". C++ signature :  bool oscillator_1_effect_mode_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def oscillator_1_wavetable_category_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "oscillator_1_wavetable_category". C++ signature :  bool oscillator_1_wavetable_category_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def oscillator_1_wavetable_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "oscillator_1_wavetable_index". C++ signature :  bool oscillator_1_wavetable_index_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def oscillator_1_wavetables_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "oscillator_1_wavetables". C++ signature :  bool oscillator_1_wavetables_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def oscillator_2_effect_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "oscillator_2_effect_mode". C++ signature :  bool oscillator_2_effect_mode_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def oscillator_2_wavetable_category_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "oscillator_2_wavetable_category". C++ signature :  bool oscillator_2_wavetable_category_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def oscillator_2_wavetable_index_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "oscillator_2_wavetable_index". C++ signature :  bool oscillator_2_wavetable_index_has_listener(TWavetableDevicePyHandle,boost::python::api::object)oscillator_2_wavetable_index_has_listener( (WavetableDevice)arg1, (object)arg2) -> bool : Returns true, if the given listener function or method is connected to the property "oscillator_2_wavetable_index". C++ signature :  bool oscillator_2_wavetable_index_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def oscillator_2_wavetables_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "oscillator_2_wavetables". C++ signature :  bool oscillator_2_wavetables_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def parameters_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "parameters". C++ signature :  bool parameters_has_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def poly_voices_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "poly_voices". C++ signature :  bool poly_voices_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def remove_filter_routing_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "filter_routing". C++ signature :  void remove_filter_routing_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_is_active_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "is_active". C++ signature :  void remove_is_active_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_modulation_matrix_changed_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "modulation_matrix_changed". C++ signature :  void remove_modulation_matrix_changed_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_mono_poly_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "mono_poly". C++ signature :  void remove_mono_poly_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_name_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "name". C++ signature :  void remove_name_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_oscillator_1_effect_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "oscillator_1_effect_mode". C++ signature :  void remove_oscillator_1_effect_mode_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_oscillator_1_wavetable_category_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "oscillator_1_wavetable_category". C++ signature :  void remove_oscillator_1_wavetable_category_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_oscillator_1_wavetable_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "oscillator_1_wavetable_index". C++ signature :  void remove_oscillator_1_wavetable_index_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_oscillator_1_wavetables_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "oscillator_1_wavetables". C++ signature :  void remove_oscillator_1_wavetables_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_oscillator_2_effect_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "oscillator_2_effect_mode". C++ signature :  void remove_oscillator_2_effect_mode_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_oscillator_2_wavetable_category_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "oscillator_2_wavetable_category". C++ signature :  void remove_oscillator_2_wavetable_category_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_oscillator_2_wavetable_index_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "oscillator_2_wavetable_index". C++ signature :  void remove_oscillator_2_wavetable_index_listener(TWavetableDevicePyHandle,boost::python::api::object)remove_oscillator_2_wavetable_index_listener( (WavetableDevice)arg1, (object)arg2) -> None : Remove a previously set listener function or method from property "oscillator_2_wavetable_index". C++ signature :  void remove_oscillator_2_wavetable_index_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_oscillator_2_wavetables_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "oscillator_2_wavetables". C++ signature :  void remove_oscillator_2_wavetables_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_parameters_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "parameters". C++ signature :  void remove_parameters_listener(TPyHandle<ADevice>,boost::python::api::object)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_poly_voices_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "poly_voices". C++ signature :  void remove_poly_voices_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_unison_mode_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "unison_mode". C++ signature :  void remove_unison_mode_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_unison_voice_count_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "unison_voice_count". C++ signature :  void remove_unison_voice_count_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def remove_visible_modulation_target_names_listener(self, arg1, arg2):
            """
            Remove a previously set listener function or method from property "visible_modulation_target_names". C++ signature :  void remove_visible_modulation_target_names_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            """
            pass

        def set_modulation_value(self, handle, target_index, source, value):
            """
            Set the value of a modulation amount for the given target-source connection. C++ signature :  void set_modulation_value(TWavetableDevicePyHandle,int,int,float)
            :param handle: handle
            :type handle: WavetableDevice
            :param target_index: target_index
            :type target_index: int
            :param source: source
            :type source: int
            :param value: value
            :type value: float
            """
            pass

        def store_chosen_bank(self, arg1, arg2, arg3):
            """
            Set the selected bank in the device for persistency. C++ signature :  void store_chosen_bank(TPyHandle<ADevice>,int,int)
            :param arg1: arg1
            :type arg1: Device
            :param arg2: arg2
            :type arg2: int
            :param arg3: arg3
            :type arg3: int
            """
            pass

        def unison_mode_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "unison_mode". C++ signature :  bool unison_mode_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def unison_voice_count_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "unison_voice_count". C++ signature :  bool unison_voice_count_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        def visible_modulation_target_names_has_listener(self, arg1, arg2):
            """
            Returns true, if the given listener function or method is connected to the property "visible_modulation_target_names". C++ signature :  bool visible_modulation_target_names_has_listener(TWavetableDevicePyHandle,boost::python::api::object)
            :param arg1: arg1
            :type arg1: WavetableDevice
            :param arg2: arg2
            :type arg2: object
            :rtype: bool
            """
            pass

        class View(object):
            def __init__(self, *a, *k):
                """
                Representing the view aspects of a Wavetable device.
                """
                pass

            @property
            def _live_ptr(self):
                pass

            @property
            def canonical_parent(self):
                """
                Get the canonical parent of the View.
                """
                pass

            @property
            def is_collapsed(self):
                """
                Get/Set/Listen if the device is shown collapsed in the device chain.
                """
                pass

            def add_is_collapsed_listener(self, arg1, arg2):
                """
                Add a listener function or method, which will be called as soon as the property "is_collapsed" has changed. C++ signature :  void add_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass

            def is_collapsed_has_listener(self, arg1, arg2):
                """
                Returns true, if the given listener function or method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                :rtype: bool
                """
                pass

            def remove_is_collapsed_listener(self, arg1, arg2):
                """
                Remove a previously set listener function or method from property "is_collapsed". C++ signature :  void remove_is_collapsed_listener(TPyViewData<ADevice>,boost::python::api::object)
                :param arg1: arg1
                :type arg1: View
                :param arg2: arg2
                :type arg2: object
                """
                pass
