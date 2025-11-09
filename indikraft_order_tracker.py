import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import font  

class OrderTrackerApp:

    MOCK_ORDER_DB = {
        "IK12345": {"status": "Shipped", "details": "Your hand-painted vase left our warehouse. Estimated delivery: Nov 10."},
        "IK67890": {"status": "Processing", "details": "Your custom block-print saree is being prepared by our artisan."},
        "IK55500": {"status": "Delivered", "details": "Your order was delivered on Nov 7."},
        "IK99999": {"status": "Order Placed", "details": "We've received your order for the 'Jaipur Blue' pottery set."}
    }

    ORDER_STEPS = ["Order Placed", "Processing", "Shipped", "Delivered"]

    def __init__(self, root):
        """
        The constructor for our app.
        'root' is the main window.
        """
        self.root = root
        root.title("Indikraft Order Tracker")
        root.geometry("800x550") 
        card_frame = tb.Frame(
            root,
            bootstyle="light",
            padding=(50, 30)
        )
        card_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        card_frame.grid_rowconfigure(0, weight=1) 
        card_frame.grid_rowconfigure(1, weight=1) 
        card_frame.grid_rowconfigure(2, weight=1) 
        card_frame.grid_rowconfigure(3, weight=2) 
        card_frame.grid_rowconfigure(4, weight=2) 
        card_frame.grid_columnconfigure(0, weight=1)

        header_font = font.Font(family="Helvetica", size=28, weight="bold")
        header_label = tb.Label(
            card_frame,
            text="Indikraft Order Tracker",
            font=header_font,
            bootstyle="primary"
        )
        header_label.grid(row=0, column=0, pady=(10, 0))

        sub_header_font = font.Font(family="Helvetica", size=14)
        sub_header_label = tb.Label(
            card_frame,
            text="Modern GUI Task",
            font=sub_header_font,
            bootstyle="secondary"
        )
        sub_header_label.grid(row=1, column=0, pady=(0, 20))

        input_frame = tb.Frame(card_frame, bootstyle="light")
        input_frame.grid(row=2, column=0, pady=10, sticky="ew", padx=50)

        input_label = tb.Label(
            input_frame,
            text="Enter Order ID:",
            font=("Helvetica", 12),
            bootstyle="dark"
        )
        input_label.pack(side="left", padx=(0, 10))

        self.order_entry = tb.Entry(
            input_frame,
            font=("Helvetica", 12),
            bootstyle="info"
        )
        self.order_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        self.order_entry.bind("<Return>", self.track_order_event)

        track_button = tb.Button(
            input_frame,
            text="Track",
            bootstyle="primary", 
            command=self.track_order
        )
        track_button.pack(side="left", padx=(5, 0))

       
        status_frame = tb.Frame(card_frame, bootstyle="light")
        status_frame.grid(row=3, column=0, pady=20, sticky="ew", padx=50)

        self.step_labels = []
        self.arrow_labels = []
        num_steps = len(self.ORDER_STEPS)

        for i, step in enumerate(self.ORDER_STEPS):
           
            step_label = tb.Label(
                status_frame,
                text=step,
                font=("Helvetica", 11, "bold"),
                padding=15,
                bootstyle="secondary", 
                anchor="center"
            )
            step_label.grid(row=0, column=i*2, sticky="ew")
            self.step_labels.append(step_label)
            
           
            if i < num_steps - 1:
                arrow_label = tb.Label(
                    status_frame,
                    text="→",
                    font=("Helvetica", 16, "bold"),
                    bootstyle="secondary", 
                    anchor="center"
                )
                arrow_label.grid(row=0, column=i*2 + 1, sticky="ew")
                self.arrow_labels.append(arrow_label)
                
                status_frame.grid_columnconfigure(i*2, weight=4) 
                status_frame.grid_columnconfigure(i*2 + 1, weight=1) 
        
       
        status_frame.grid_columnconfigure((num_steps - 1) * 2, weight=4)

        self.status_details_frame = tb.Frame(
            card_frame,
            bootstyle="secondary",
            padding=20
        )
        self.status_details_frame.grid(row=4, column=0, pady=(10, 20), sticky="ew", padx=50)

        self.status_details_label = tb.Label(
            self.status_details_frame,
            text="Please enter an Order ID to begin tracking.",
            font=("Helvetica", 12, "italic"),
            bootstyle="inverse-secondary", 
            wraplength=600,
            justify="center"
        )
        self.status_details_label.pack(fill="x", expand=True)

  
    
    def track_order_event(self, event):
        """Helper function to handle the <Return> key event"""
        self.track_order()

    def track_order(self):
        """
        This function is called when the 'Track' button is pressed.
        It contains all the logic for tracking the order.
        """
        order_id = self.order_entry.get().strip().upper()

        
        for label in self.step_labels:
            label.config(bootstyle="secondary")
        for label in self.arrow_labels:
            label.config(bootstyle="secondary")
            
        self.status_details_frame.config(bootstyle="secondary")
        self.status_details_label.config(
            text="Please enter an Order ID to begin tracking.",
            font=("Helvetica", 12, "italic"),
            bootstyle="inverse-secondary"
        )

        if order_id in self.MOCK_ORDER_DB:
            order_data = self.MOCK_ORDER_DB[order_id]
            current_status = order_data["status"]
            details = order_data["details"]

            try:
                current_step_index = self.ORDER_STEPS.index(current_status)
                for i in range(current_step_index + 1):
                    self.step_labels[i].config(bootstyle="success")
                   
                    if i < len(self.arrow_labels):
                        self.arrow_labels[i].config(bootstyle="success")

            except ValueError:
                
                self.status_details_frame.config(bootstyle="danger")
                self.status_details_label.config(
                    text=f"Error: Unknown status '{current_status}'.",
                    bootstyle="inverse-danger",
                    font=("Helvetica", 12)
                )
                return

            self.status_details_frame.config(bootstyle="info")
            self.status_details_label.config(
                text=f"Status: {current_status}\n{details}",
                bootstyle="inverse-info",
                font=("Helvetica", 12)
            )

        else:
           
            self.status_details_frame.config(bootstyle="danger")
            self.status_details_label.config(
                text=f"Order ID '{order_id}' not found. Please check the ID and try again.",
                bootstyle="inverse-danger", 
                font=("Helvetica", 12)
            )

if __name__ == "__main__":
    
    root = tb.Window(themename="morph")
    root.config(bg=root.style.colors.get('secondary'))
    
    app = OrderTrackerApp(root)
    root.mainloop()