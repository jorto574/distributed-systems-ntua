import sys
import matplotlib.pyplot as plt

# Check if the capacity argument is provided
if len(sys.argv) < 2:
    print("Usage: python script_name.py <capacity>")
    sys.exit(1)

capacity = int(sys.argv[1])
x = [5, 10]

y = []

if capacity == 5:
    y = [38.14612848132771, 41.255512754396705]

elif capacity == 10:
    y = [41.11840625079959, 46.15554945646096]

elif capacity == 20:
    y = [43.91754194350042, 50.25185930384198]

# Plot
plt.bar(x, y)

# Title and labels
plt.title(f"Capacity {capacity}")
plt.xlabel("Clients")
plt.ylabel("Throughput")

# Save the plot
plt.savefig(f"capacity_{capacity}_throughput.png")
