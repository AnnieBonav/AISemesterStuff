import pandas as py, pygame, matplotlib.pyplot as plt, time

worldCities = py.read_csv('./RBFS/worldcities.csv', usecols=['city', 'lat', 'lng', 'country', 'admin_name'])

def createCountryDF(countryName, citiesPerState = 1):
    countryDF = worldCities.copy()
    countryDF = countryDF[countryDF['country'] == countryName]
    countryDF = countryDF.groupby('admin_name').head(citiesPerState)
    countryDF['state'] = 'closed'
    countryDF = countryDF.reset_index(drop=True)
    return countryDF

mexicoCities = createCountryDF("Mexico")
mexicoCities['state'].loc[mexicoCities['city'] == 'Mexico City'] = 'open'
print(mexicoCities.head())


# plt.scatter(mexicoDF['lng'], mexicoDF['lat'])
# plt.show()
mapToUse = [mexicoCities, "Mexico"]

sleepTime = 1

def RunPygame(mapToUse):
    map = mapToUse[0]
    mapName = mapToUse[1]
    # Initialize Pygame
    pygame.init()

    # Define colors
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    gray = (200, 200, 200)
    white = (255, 255, 255)
    
    font = pygame.font.Font(None, 36)
    titleText = font.render(f"{mapName}'s Map", True, black)
    visitedNodeText = font.render("Visited Node:", True, black)

    # Set the width and height of the screen
    screenWidth = 1200
    screenHeight = 800
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption(f"{mapName} Map Visualization")

    textWidth = titleText.get_width()
    textHeight = titleText.get_height()
    
    screenWidth *= .9
    screenHeight *= .9
    # Scale the latitude and longitude values to fit the screen
    min_lat = map['lat'].min()
    max_lat = map['lat'].max()
    min_lng = map['lng'].min()
    max_lng = map['lng'].max()

    scaled_lat = (map['lat'] - min_lat) / (max_lat - min_lat) * screenHeight
    print("Info", type(scaled_lat))

    scaled_lng = (map['lng'] - min_lng) / (max_lng - min_lng) * screenWidth
    scaled_lat = screenHeight - scaled_lat
    # Game loop
    running = True

    counter = 0
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(white)

        # Draw the points
        for lat, lng, state in zip(scaled_lat + screenWidth/10, scaled_lng + screenHeight/10, map['state']):
            match (state):
                case "open":
                    color = red
                case "closed":
                    color = black
                case "frontier":
                    color = blue
                case _:
                    color = gray
            pygame.draw.circle(screen, color, (int(lng), int(lat)), 8)

        # Update the screen
        textX = (screenWidth - textWidth) // 2
        textY = 20
        screen.blit(titleText, (textX, textY))

        textY = 40
        screen.blit(visitedNodeText, (40, textY))

        
        visitedNodeText = font.render("Visited Node: " + str(counter), True, black)
        counter += 1
        if(counter%2 == 0):
            map['state'].loc[map['city'] == 'Mexico City'] = 'closed'
        else:
            map['state'].loc[map['city'] == 'Mexico City'] = 'frontier'


        pygame.display.flip()

        time.sleep(sleepTime)
        print("Slept")
    # Quit Pygame
    pygame.quit()

RunPygame(mapToUse)