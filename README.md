# QRCode-Generator

QRCode-Generator is a Python application built with Tkinter that allows users to manage data and generate QR codes. It supports adding, editing, viewing, and deleting data through a user-friendly interface. Additionally, users can upload a CSV file to populate the data. By double-clicking a row in the table, the corresponding QR code is displayed in a separate frame.

## Features

- **QR Code Generation:** Generate QR codes for each entry in the table.
- **Data Management:** Add, edit, view, and delete data.
- **CSV Upload:** Upload a CSV file to populate the table.
- **Interactive Table:** Double-click on a row to view the generated QR code.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/QRCode-Generator.git
   cd QRCode-Generator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## How to Use

1. **Adding Data:**
   - Use the "Add" button to input new data into the table.

2. **Editing Data:**
   - Select a row and click the "Edit" button to modify the data.

3. **Viewing QR Code:**
   - Double-click on any row in the table to display its corresponding QR code in the dedicated frame.

4. **Deleting Data:**
   - Select a row and click the "Delete" button to remove the entry.

5. **Uploading CSV:**
   - Use the "Upload CSV" button to upload a CSV file and populate the table with its data.

## Screenshots

![Main Interface](path/to/screenshot_main.png)
*Main interface showcasing the table and QR code display.*

![QR Code View](path/to/screenshot_qrcode.png)
*QR code displayed upon double-clicking a row.*

## Requirements

- Python 3.8+
- Tkinter (built-in with Python)
- Pillow (for handling images)
- qrcode (for generating QR codes)
- pandas (for handling CSV files)

## File Structure

```
QRCode-Generator/
├── main.py               # Main application file
├── requirements.txt      # List of dependencies
├── README.md             # Project documentation
├── assets/               # Contains screenshots and other assets
└── data/                 # Example CSV files
```

## Contributing

Contributions are welcome! If you have ideas or improvements, feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add a new feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Happy coding!
