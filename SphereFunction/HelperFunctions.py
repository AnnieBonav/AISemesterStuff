import csv
from datetime import datetime
from matplotlib import pyplot as plt

def saveDataToCsv(filePath, allData):
    stringData = ""
    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for data in allData:
        stringData += data + ","

    with open(filePath, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([stringData, currentTime])


def visualization():
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define the number of points
    num_points = 100

    # Define the angles
    theta = np.linspace(0, 2.*np.pi, num_points)
    phi = np.linspace(0, 2.*np.pi, num_points)

    # Create a 2D grid of angles
    theta, phi = np.meshgrid(theta, phi)

    # Define the radius
    r = 1

    # Calculate the x, y, and z coordinates of the points on the sphere
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)

    # Plot the sphere
    ax.plot_surface(x, y, z, color='b')
    plt.show()