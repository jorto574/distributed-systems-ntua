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
    y = [0.1260335582953233, 0.11999596463571681]

elif capacity == 10:
    y = [0.24320008754730224, 0.21034822417694388]

elif capacity == 20:
    y = [0.4949987971264383, 0.4145783583323161]

# Plot
plt.bar(x, y)

# Title and labels
plt.title(f"Capacity {capacity}")
plt.xlabel("Clients")
plt.ylabel("Block time")

# Save the plot
plt.savefig(f"capacity_{capacity}_block_time.png")
