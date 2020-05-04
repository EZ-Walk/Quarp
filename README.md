# Quarp
Qualitative Response Projects is a series of classes that are aimed at extracting the meat and potatoes from qualitative form responses

## Versions
- 1.0 - Released May 4, 2020. Contains the Response class and cleanAndCluster class. These are applied by creating an Quarp object on a qualitative column and then using a guided clustering technique to train the algorithm to find certain valued attributes fo a response. Running this algorithm on the spring 2020 IFC registration list yielded the following results.
  Responses: 418
  Manual Classifications: 27
  Guessed Parents: 298
  Discarded Fragments: 5
  Percent of parents detected without manual intervention: 92.344498%
  
  The algorithm could be improved drastically by teaching it to handle multi word parents. In this test case these would be "cross country", "water polo", and "national honor society".
