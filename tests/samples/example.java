/*
 * Copyright (C) 2020 Arm Mbed. All rights reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import static org.junit.Assert.fail;

import java.util.Arrays;

import io.reactivex.BackpressureStrategy;


public class Banana extends Fruit {

    /**
     * Foos a Bar.
     * <p>
     * Note: This example introduces new high level abstraction objects
     */

    @Example
    public void fooABar() {
        Wibble wibbler = new Wobble(config);
        try {
            // an example: number 1
            // For more information about backpressure strategies, please have a look at related documentation:
            // https://github.com/ReactiveX/RxJava/wiki/Backpressure
            wibbler.subscribe(
                    Thing1.newFilter().likeDevice("016%")
                            .inDeviceStates(Arrays.asList(DeviceState.A, DeviceState.B)),
                    BackpressureStrategy.BUFFER).flow().subscribe(System.out::println);

            // Listening to device state changes for 2 minutes.
            Thread.sleep(120000);

            // Stopping the Wobble.
            wibbler.stop();
            // end of example

        } catch (Exception e) {
            e.printStackTrace();
            fail(e.getMessage());
        }
    }
}