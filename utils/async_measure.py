##################################################################################################################
# ASYNCHRONOUS MEASUREMENT
##################################################################################################################

import time
import asyncio

async def async_measure(spec, osc, tc):
    '''
    function to get measurements from all devices asynchronously to optimize
    time to get measurements

    Inputs:
    osc         initialized Oscilloscope instance
    spec        Spectrometer device reference

    Outputs:
    tasks       completed list of tasks containing data measurements; the first
                task obtains spectrometer measurements, second task gets oscilloscope
                measurements
    runTime     run time to complete all tasks
    '''
    # create list of tasks to complete asynchronously
    tasks = [asyncio.create_task(async_get_osc(osc)),
            asyncio.create_task(async_get_spectra(spec)),
             asyncio.create_task(async_get_tc(tc))]  


    startTime = time.perf_counter()
    await asyncio.wait(tasks)
    # await asyncio.gather(*tasks)
    endTime = time.perf_counter()
    runTime = endTime-startTime
    # print time to complete measurements
    print(f'        ...completed data collection tasks after {runTime:0.4f} seconds')
    return tasks, runTime


async def async_get_spectra(spec):
    '''
    asynchronous definition of capturing optical emission spectra data
    Inputs:
    spec                Spectrometer device

    Outputs:
    intensities         intensities
    wavelengths         wavelengths that correspond to the intensities
    '''
    if spec is None:
        await asyncio.sleep(0.2)
        intensities = None
        wavelengths = None
    else:
        intensities = spec.intensities()
        wavelengths = spec.wavelengths()
    return [wavelengths, intensities]


async def async_get_osc(osc):
    '''
    asynchronous definition of oscilloscope measurements
    Inputs:
    osc         the oscilloscope object as defined in its Class definition

    Outputs:
    t           time vector for the measurements
    osc_data    list of dictionaries of data from the oscilloscope; each dictionary
                contains data from one channel
    '''
    if osc is None:
        await asyncio.sleep(0.1)
        t = None
        osc_data = None
    else:
        t, osc_data = osc.collect_data_block()
    return [t, osc_data]
async def async_get_tc(tc):
    '''
    asynchronous definition of capturing thermal camera data
    Inputs:
    tc          the thermal camera object as defined in its Class definition

    Outputs:
    temp        Surface temperature
    '''
    if tc is None:
        await asyncio.sleep(0.1)
        temp = None
    else:
        temp = await tc.getSurfaceTemperature(True, True)
        return temp
