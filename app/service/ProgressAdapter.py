from tkinter import Tk
from tkinter.ttk import Progressbar, Style


# UI Components
class ProgressIndicator:
    """Progress bar UI component for the thumbnail loading UI."""

    def __init__(self, root: Tk):
        """Initialize the progress indicator with a sleek, professional appearance.
        
        Args:
            root: The Tkinter root window to attach the progress indicator to
        """
        self.root = root
        self.processed_count = 0
        self.total_items = 0
        
        # Apply professional styling with material design influences
        self.style = Style()
        print(self.style.theme_names())
        self.style.theme_use("classic")
        self.style.configure(
            "Professional.Horizontal.TProgressbar",
            
            background='#1976D2',   # Material design primary blue
            thickness=16,           # Balanced thickness
            borderwidth=0,          # Clean edges
            borderradius=8          # Subtle rounded corners
        )
        
        # Create a visually balanced progress bar
        self.progress_bar = Progressbar(
            root,
            orient='horizontal',
            length=380,
            mode='determinate',
            style="Professional.Horizontal.TProgressbar"
        )
        
        # Position with proper spacing for visual harmony
        self.progress_bar.grid(
            row=0, 
            column=0, 
            padx=10, 
            pady=(15, 15), 
            sticky='ew'
        )
        
        # Ensure responsive layout
        root.grid_columnconfigure(0, weight=1)

    def set_total(self, total: int) -> None:
        """Set the total number of items to process.
        
        Args:
            total: The total number of items to be processed
        """
        self.total_items = total

    def increment(self) -> None:
        """Increment progress by one step. Thread-safe implementation."""
        self.root.after(0, self._update_progress)

    def _update_progress(self) -> None:
        """Update the progress bar state."""
        self.processed_count += 1
        self.progress_bar.configure(value=(self.processed_count / self.total_items) * 100)
        
        # Handle completion with a professional fade-out
        if self.processed_count >= self.total_items:
            # Provide visual feedback before closing
            self.root.after(800, self.root.destroy)

