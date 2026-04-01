from fractions import Fraction

def afisare_tabel(self):
        """Prints a console table representation of the game matrix, matching image_0.png structure."""
        n_rows, n_cols = self.MatriceQ.shape
        sub_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉") # Unicode subscripts

        def format_val(val):
            """Simplified fraction formatter for game values."""
            if abs(val) < 1e-9: return "0"
            return str(Fraction(float(val)).limit_denominator(1000))

        # --- Prepare data as strings ---
        # Top headers
        tl_label = "A \\ B"
        b_labels = [f"b{j+1}".translate(sub_map) for j in range(n_cols)]
        tr_label = "α = MIN(L)"

        # Left labels
        a_labels = [f"a{i+1}".translate(sub_map) for i in range(n_rows)]
        bl_label = "β = MAX(C)"

        # Payoff matrix values and row/col stats
        matrix_str = [[format_val(self.MatriceQ[i, j]) for j in range(n_cols)] for i in range(n_rows)]
        alpha_str = [format_val(a) for a in self.alpha]
        beta_str = [format_val(b) for b in self.beta]

        # Corner cells - plain text approximation of diagonal split
        # We form the string for the combined bottom-right cell
        v1_val_str = format_val(self.v1)
        v2_val_str = format_val(self.v2)
        
        # Calculate cell data lengths to center combined string
        v_combined_label = f"v\u2081={v1_val_str} / v\u2082={v2_val_str}" # Visual separator idea

        # --- Calculate column widths ---
        col_widths = []

        # Leftmost column width
        left_width = max(len(tl_label), len(bl_label), max(len(l) for l in a_labels)) + 2
        col_widths.append(left_width)

        # Payoff column widths
        for j in range(n_cols):
            # Width is max of: col label, any value in col, or col max
            max_val_len = max(len(format_val(self.MatriceQ[i, j])) for i in range(n_rows))
            w = max(len(b_labels[j]), max_val_len, len(beta_str[j])) + 2
            col_widths.append(w)

        # α column width
        # This will contain the α header, all α values, AND the diagonally split text
        alpha_width = max(len(tr_label), max(len(s) for s in alpha_str), len(f"v\u2081={v1_val_str}"), len(f"v\u2082={v2_val_str}"), len(v_combined_label)) + 2
        col_widths.append(alpha_width)

        # --- Construct separators ---
        sep_char = " | "
        table_width = sum(col_widths) + (len(col_widths) - 1) * len(sep_char)
        line_sep = "-" * table_width

        # --- Build and Print Table ---
        # Print top header line
        header = f"{tl_label:^{left_width}}" + sep_char
        header += sep_char.join(f"{b:^{w}}" for b, w in zip(b_labels, col_widths[1:-1])) + sep_char
        header += f"{tr_label:^{alpha_width}}"
        print(f"\n{header}")
        print(line_sep)

        # Print payoff and α rows
        for i in range(n_rows):
            row_data = f"{a_labels[i]:>{left_width}}" + sep_char
            # Matrix values centered
            row_data += sep_char.join(f"{val:^{w}}" for val, w in zip(matrix_str[i], col_widths[1:-1])) + sep_char
            # α values on the right
            row_data += f"{alpha_str[i]:>{alpha_width}}"
            print(row_data)

        print(line_sep)

        # Print bottom row (β maxima) and special split cell
        bottom_row = f"{bl_label:^{left_width}}" + sep_char
        bottom_row += sep_char.join(f"{b:^{w}}" for b, w in zip(beta_str, col_widths[1:-1])) + sep_char
        
        # Diagonally split text approximation
        # We print it as centered plain text within the last cell width
        bottom_row += f"{v_combined_label:^{alpha_width}}"
        print(bottom_row)
        print("=" * table_width + "\n")