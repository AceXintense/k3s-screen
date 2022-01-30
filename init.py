import modules.core as core
import modules.kubernetes as kubernetes
import modules.glances as glances
import app.utilities as utilities
import app.application as application

slide = 0
slides = [
    glances.get_cpu_page,
    glances.get_swap_memory_page,
    glances.get_cpu_load_page,
    core.get_temperature_page,
    core.get_usage_page,
    kubernetes.get_page,
]
maxSlide = len(slides) - 1

def on_update(screen):
    global slides, slide, maxSlide
    changeSlide = int(application.get_tick() % 5)  # If the number is divisible by 5 then it will be 0
    if (changeSlide == 0):
        if (slide < maxSlide):
            slide = (slide + 1)
        else:
            slide = 0
    
    slides[slide](screen)

    utilities.log("Tick: " + str(application.get_tick()))
    utilities.log("Change slide: " + str(changeSlide))
    utilities.log("Slide: " + str(slide))
    utilities.log("Max Slide: " + str(maxSlide))

    utilities.log("Hostname: " + core.get_hostname())
    utilities.log("Local IP: " + core.get_local_ip())
    utilities.log("CPU Temp: " + core.get_cpu_temperature())
    utilities.log("CPU Usage: " + core.get_cpu_useage())
    utilities.log("Memory Usage: " + core.get_memory_useage())

application.setup(on_update)