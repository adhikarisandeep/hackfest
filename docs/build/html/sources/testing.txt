Testing
-------

We will need to extensively test our programs to ensure that they
actually work on the day of the competition. To this end, we will
create a suite of unit tests for each component. Since the final
design of each component is subject to change, these tests will need
should not be based around the actual implementation of each
component, but instead on the interface used to interact with the
component.

The following is brief listings of some of the possible unit tests
specific to each component.

 * Scoring Server - Create a test network that implements the
   necessary services and see if the scoring server is able to accurately
   test these services.

 * Client Server - Create some simulated data similar to the output of
   the scoring server and see if the client server is able to handle this
   data correctly and display the appropriate information.

 * Chat mechanism - Create some dummy clients that chat back and forth
   and test the output on both ends for correctness.

 * Challenge Servers - Have these programs act on a test network and
   simulate the appropriate events.
