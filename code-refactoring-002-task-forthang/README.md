# Refactoring for testability in C++ 

> 
> Main repository took from https://github.com/platisd/refactoring-for-testability-cpp to educational purpose

Hard-to-test patterns in C++ and how to refactor them.

### Contents

* [What](#what)
* [Why](#why)
* [How](#how)
* [Hard-to-test patterns](#hard-to-test-patterns)
  * [Hardcoded dependencies](#hardcoded-dependencies)
  * [Time](#time)
  * [Singletons](#singletons)

## What

This repository includes examples of code that is *tricky* to unit test.
The difficulty, in the context of this work, does **not** lie in its
inherent complexity when it comes to the logic or domain. For example,
software that has many branches or tries to solve a problem that needs to
follow a set of convoluted business rules, will not be examined. In fact,
all of the examples are rather simple.

The focus will be on patterns *technically* difficult to unit test
because they:
* Require irrelevant software to be tested too
  * E.g.: 3rd party libraries, classes other than the one under test
* Delay the test execution
  * E.g.: sleeps inside code under test
* Require intricate structures to be copied or written from scratch
  * E.g.: Fakes containing a lot of logic
* Require test details to be included in the production code
  * E.g.: `#ifdef UNIT_TESTS`
* Make changes and/or are dependent on the runtime environment
  * E.g.: Creating or reading from files

## Why

If the code is testable, writing unit tests can be particularly fun.
It can be seen as a satisfying way to *prove* your effort is correct _in
principle_. Of course, writing unit tests does not necessarily imply
your software works as a whole, especially in conjunction with other
parts of the system. To ensure this you should look into other types of
testing, where larger pieces of functionality get verified. The most
important thing to remember is all of these tests should be *automated*.

When it comes to unit tests, you should author **testable** code that can
be verified with small and atomic tests. You should not have to test
unrelated logic nor implement complex functionality just to be able to test.
After all, unit testing should be fun and give you the confidence to develop
without worrying you "broke" something.

The three main reasons behind untestable or hard to test code, in a
not-so-random order are:

1. Project management does not care about quality
2. Developers do not know how to write testable code
3. Domain constraints on the design and technology

The latter (3), is sometimes an excuse brought forward by developers from
(2) so it needs to be taken with a grain of salt by the management if they
do not want to be part of (1).

## How

Writing testable code, does not fundamentally differ from writing *good*
code. It is however much easier to produce such code, if you write it along
or *after* your unit tests ([TDD](https://en.wikipedia.org/wiki/Test-driven_development)).
Whatever your approach may be, as a rule of thumb, writing code according to
the following guidelines and design principles, will in most cases result
in easy-to-test software:
* Write [SOLID](https://en.wikipedia.org/wiki/SOLID) code
* Prefer [Composition over inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance)
  * [C.120](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c120-use-class-hierarchies-to-represent-concepts-with-inherent-hierarchical-structure-only)
  * [C.121](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c121-if-a-base-class-is-used-as-an-interface-make-it-a-pure-abstract-class)
  * [C.129](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c129-when-designing-a-class-hierarchy-distinguish-between-implementation-inheritance-and-interface-inheritance)
  * [C.133](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c133-avoid-protected-data)
  * [I.25](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Ri-abstract)
  * [NR.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nr7-dont-make-all-data-members-protected)
* Avoid static and global elements
  * [I.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#i2-avoid-non-const-global-variables)
  * [I.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#i3-avoid-singletons)
  * [I.22](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Ri-global-init)
* Write code without side effects
  * [Con.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconst-immutable)
  * [Con.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#con2-by-default-make-member-functions-const)
  * [Con.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#con3-by-default-pass-pointers-and-references-to-consts)
  * [Con.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#con4-use-const-to-define-objects-with-values-that-do-not-change-after-construction)
  * [NR.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nr5-dont-use-two-phase-initialization)
  * [C.40](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c40-define-a-constructor-if-a-class-has-an-invariant)
  * [C.41](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c41-a-constructor-should-create-a-fully-initialized-object)
* Abstract away code that cannot or should not be tested
  * E.g.: 3rd party libraries, time, file operations, other classes etc

## Hard-to-test patterns

The patterns or, if you may, *concepts*, are organized in directories named
after their subject and are outlined below. These concepts are fundamentally
difficult to test but please keep in mind this is not necessarily the only
way to do so. Moreover, with the introduction of more feature-rich testing
frameworks, dependency injection containers etc, there may be ways to get
around the inherent lack of testability of these examples. That being said,
it is good to know how to refactor them according to object oriented design
best practices as well as the C++ Core guidelines. We illustrate this by relying
only on [GoogleTest](https://github.com/google/googletest). GoogleTest, which
includes mocking via GoogleMock is a lightweight testing framework and probably
the de facto standard for C++.

The solutions proposed, do not claim to be better in performance nor compliant
with any safety critical coding guidelines your project may have. They tackle
the lack of testability at a software design level and do not take into
account special domain constraints. Nonetheless, if performance is brought
forward as an argument against testable code, before taking any decisions
please refer to the [3 rules of optimization](https://wiki.c2.com/?RulesOfOptimization).

The code examples use `CMake` and need a compiler that supports C++17 or later.
In most cases they include the code `before` and `after` the refactoring efforts
in the same file under different *namespaces*. This is done for the sake of
simplicity and has the side-effect of having including indications to code smells
in the build configuration. These indications are typically followed by
comments that point them out. What is perhaps most interesting is that the
API does not change. Therefore, assuming you have well-thought APIs for your
classes then you should be able to *contain* the refactoring changes.

All the examples are runnable and inspired by real-life situations.

### [Hardcoded dependencies](020-hardcoded_dependencies)

Hardcoding dependencies results in having to include *unrelated*, to our unit under
test, code in our test setup. Consequently, we end up testing more than we should
and particularly code that has likely been tested before. This also means our test
cases are no longer *atomic*. Testing aside, our implementation is tightly coupled
to another implementation which reduces its reusability. Additionally, changes in
the implementation of the hardcoded dependencies may trigger changes in our unit
under test, which reduces maintainability and hinders software evolution.

There are two ways we may end up in this situation:
1. Using *concrete* classes
2. Extending *concrete* classes

#### Example(s)

```cpp
// Using a concrete class
struct DirectionlessOdometer
{
    DirectionlessOdometer(int pulsePin, int pulsesPerMeter);

    double getDistance() const;

protected:
    const int mPulsesPerMeter;
    int mPulses{0};
    MyInterruptServiceManager mInterruptManager;
};

DirectionlessOdometer::DirectionlessOdometer(int pulsePin, int pulsesPerMeter)
    : mPulsesPerMeter{pulsesPerMeter}
{
    mInterruptManager.triggerOnNewPulse(pulsePin, [this]() { mPulses++; });
}

double DirectionlessOdometer::getDistance() const
{
    return mPulses == 0 ? 0.0 : static_cast<double>(mPulsesPerMeter) / mPulses;
}

// Extending (and using) a concrete class
struct DirectionalOdometer : public DirectionlessOdometer
{
    DirectionalOdometer(int directionPin, int pulsePin, int pulsesPerMeter);

private:
    MyPinReader mPinReader;
    const int mDirectionPin;
};

DirectionalOdometer::DirectionalOdometer(int directionPin,
                                         int pulsePin,
                                         int pulsesPerMeter)
    : DirectionlessOdometer(pulsePin, pulsesPerMeter)
    , mDirectionPin{directionPin}
{
    mInterruptManager.triggerOnNewPulse(pulsePin, [this]() {
        if (mPinReader.read(mDirectionPin))
        {
            mPulses++;
        }
        else
        {
            mPulses--;
        }
    });
}
```

#### Alternative(s)

We separate the *common* functionality in a new class and stop extending
the concrete class. This has the added semantic benefit of avoiding to impose
a parent-child relationship. After all, a `DirectionalOdometer` is *not* really
a `DirectionlessOdometer`, is it?<br>
Then, we *inject* the *abstracted* resources that are being used into the classes
that use them via the respective constructors.

```cpp
struct Encoder
{
    virtual ~Encoder() = default;

    virtual void incrementPulses()     = 0;
    virtual void decrementPulses()     = 0;
    virtual double getDistance() const = 0;
};

struct DirectionlessOdometer
{
    DirectionlessOdometer(Encoder& encoder,
                          InterruptServiceManager& interruptServiceManager,
                          int pulsePin);

    double getDistance() const;

private:
    Encoder& mEncoder;
};

struct DirectionalOdometer
{
    DirectionalOdometer(Encoder& encoder,
                        InterruptServiceManager& interruptServiceManager,
                        PinReader& pinReader,
                        int directionPin,
                        int pulsePin);

    double getDistance() const;

private:
    Encoder& mEncoder;
    PinReader& mPinReader;
};
```

| Refactored file(s)                                                                        | Unit tests                                       |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------ |
| [DirectionlessOdometer.hpp](020-hardcoded_dependencies/include/DirectionlessOdometer.hpp) | [Odometers_test.cpp](test/ut/Odometers_test.cpp) |
| [DirectionlessOdometer.cpp](020-hardcoded_dependencies/src/DirectionlessOdometer.cpp)     |                                                  |
| [DirectionalOdometer.hpp](020-hardcoded_dependencies/include/DirectionalOdometer.hpp)     |                                                  |
| [DirectionlessOdometer.cpp](020-hardcoded_dependencies/src/DirectionalOdometer.cpp)       |                                                  |

### [Time](050-time)

Very often we need to perform operations that involve time. For example, we may need
to execute some actions at a specific interval, wait until another event happens, a
timeout expires etc. Writing code for this is very straight forward unlike testing it.
To begin with, one should be able to execute unit tests fast to quickly verify the new
functionality they are introducing to the project. Therefore, *waiting* for things
to happen, can significantly delay the test feedback loops. To make things worse, the
period we need to wait might be arbitrarily large (e.g. hours or days) which would deem
any related functionality unfit for unit tests.

#### Example(s)

```cpp
bool PowerController::turnOn()
{
    mPinManager.setPin(kPin);
    std::this_thread::sleep_for(1s);
    mPinManager.clearPin(kPin);

    std::unique_lock<std::mutex> lk(mRunnerMutex);

    mConditionVariable.wait_for(
        lk, 10s, [this]() { return mPulseReceived.load(); });

    return mPulseReceived.load();
}
```

#### Alternative(s)

Testing `turnOn` means we would have to wait for at least 1 second for every test. To
verify we would actually block the execution and wait until the timeout expires, we
would have to wait even longer. If you contemplate upon it, the *actual waiting is not
part of our logic, but a requirement of whatever receives the pulse and sends back a
signal. Instead, we should abstract the time-related operations behind two interfaces.
One that simply "keeps time" or merely blocks the current thread and another to *schedule*
events, such as the timeout expiry.

```cpp
struct TimeKeeper
{
    virtual ~TimeKeeper() = default;

    virtual void sleepFor(std::chrono::milliseconds delay) const = 0;
};

class AsynchronousTimer
{
public:
    virtual ~AsynchronousTimer() = default;

    virtual void schedule(std::function<void()> task,
                          std::chrono::seconds delay)
        = 0;
    virtual void abort() = 0;
};

bool PowerController::turnOn()
{
    mPinManager.setPin(kPin);
    mTimeKeeper.sleepFor(1s);
    mPinManager.clearPin(kPin);

    mAsynchronousTimer.schedule(
        [this]() {
            mPulseTimedOut = true;
            mConditionVariable.notify_one();
        },
        10s);

    std::unique_lock<std::mutex> lk(mRunnerMutex);

    mConditionVariable.wait(lk, [this]() {
        return mPulseReceived.load() || mPulseTimedOut.load();
    });

    mAsynchronousTimer.abort();
    mPulseTimedOut = false;

    return mPulseReceived.load();
}
```

| Refactored file(s)                                          | Unit tests                                                   |
| ----------------------------------------------------------- | ------------------------------------------------------------ |
| [PowerController.hpp](050-time/include/PowerController.hpp) | [PowerController_test.cpp](test/ut/PowerController_test.cpp) |
| [PowerController.cpp](050-time/src/PowerController.cpp)     |                                                              |

### [Singletons](080-singletons)

Try to avoid singletons ([I.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#i3-avoid-singletons)).
They have negative implications on multiple levels and their issues are well documented.
Therefore, it comes to little surprise they are also difficult to test. As a singleton *user*,
giving the test fixture access to the singleton instance is not straight forward or even
possible without some nasty workarounds. As a singleton *publisher*, and depending on how you
implemented your singleton, your test cases are likely to be affecting each other. Consequently,
they may become more complicated just to ensure they are immune to the pattern's quirks.

#### Example(s)

```cpp
struct CounterSingleton
{
    CounterSingleton(const CounterSingleton&) = delete;
    CounterSingleton(CounterSingleton&&)      = delete;
    CounterSingleton& operator=(const CounterSingleton&) = delete;
    CounterSingleton& operator=(CounterSingleton&&) = delete;

    void increment();
    void decrement();
    int get() const;

    static CounterSingleton& getInstance();

private:
    CounterSingleton() = default;

    std::atomic<int> mCounter{0};
};

CounterSingleton& CounterSingleton::getInstance()
{
    static CounterSingleton instance;

    return instance;
}

void countTo(int number)
{
    // Hard to test context
    auto& counter        = CounterSingleton::getInstance();
    bool shouldIncrement = counter.get() < number;

    while (counter.get() != number)
    {
        if (shouldIncrement)
        {
            counter.increment();
        }
        else
        {
            counter.decrement();
        }
    }
}
```

#### Alternative(s)

Ideally, you would remove the singletons from your code-base. Instead of having your classes
acquire the common resource, you should inject the common resource to them. After all, why
must your class care whether the resource it uses is also used elsewhere?

Anyway, let's assume you thought it through and concluded that removing the singletons is not
feasible. For example, the overall code structure/framework may not be facilitating the injection
of resources. Additionally, the singleton has been created by a third party, so it is not easy or
possible to drastically change their code.

To remedy the situation, you need to **isolate** the hard-to-test part of getting a hold of the
singleton instance. Then, you can skip unit testing this. Instead, once you have gotten hold of
the instance, you should inject it to your business logic which you *can* test. Of course, before
injecting it you need to have the appropriate abstractions in place. You can do this either by
having your instance implement an interface or, if that is not practical, have a wrapper class
around it that implements the said interface.

##### Wrapper class around singleton instance

```cpp
struct Counter
{
    virtual ~Counter()       = default;
    virtual void increment() = 0;
    virtual void decrement() = 0;
    virtual int get() const  = 0;
};

struct CommonCounter : public Counter
{
    CommonCounter(CounterSingleton& counterSingleton);

    void increment() override;
    void decrement() override;
    int get() const override;

private:
    CounterSingleton& mCounterSingleton;
};

struct CounterManager
{
    CounterManager(Counter& counter);

    void countTo(int number);

private:
    Counter& mCounter;
};

void CounterManager::countTo(int number)
{
    // Easy to test context
    bool shouldIncrement = mCounter.get() < number;

    while (mCounter.get() != number)
    {
        if (shouldIncrement)
        {
            mCounter.increment();
        }
        else
        {
            mCounter.decrement();
        }
    }
}
```

##### Singleton instance implements an interface

```cpp
struct CounterSingleton : public Counter
{
    CounterSingleton(const CounterSingleton&) = delete;
    CounterSingleton(CounterSingleton&&)      = delete;
    CounterSingleton& operator=(const CounterSingleton&) = delete;
    CounterSingleton& operator=(CounterSingleton&&) = delete;

    void increment() override;
    void decrement() override;
    int get() const override;

    static CounterSingleton& getInstance();

private:
    CounterSingleton() = default;

    std::atomic<int> mCounter{0};
};
```
| Refactored file(s)                                                  | Unit tests                                                 |
| ------------------------------------------------------------------- | ---------------------------------------------------------- |
| [CounterSingleton.hpp](080-singletons/include/CounterSingleton.hpp) | [CounterManager_test.cpp](test/ut/CounterManager_test.cpp) |
| [CounterSingleton.cpp](080-singletons/src/CounterSingleton.cpp)     |                                                            |
