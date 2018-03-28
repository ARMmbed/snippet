```python
# example: number 1
print('x: 5')
for number in range(5):
    print(number)
```
```java
# example: number 1
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
```