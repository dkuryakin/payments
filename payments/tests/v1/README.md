Sorry guys, but I have no much time for implementing 
good tests coverage. So I only implement one 
end-to-end test just for instance.

Actually we need many layers of tests in production:
 * unit tests - to test each function and/or data type.
   These ones are not actually so good for real testing
   of complex pipelines. They only can highlight dummy
   bugs. 
 * integration tests - to test how different parts of 
   pipeline works together. It's actually testing of 
   interfaces abstraction layer. Quite useful type of 
   tests.
 * end-to-end tests - to test entire pipeline. It's the 
   best type of tests for complex pipelines, I suppose.
   So, it's must have.
 * load tests - to test behavior of pipeline under high
   load. Also must have.
