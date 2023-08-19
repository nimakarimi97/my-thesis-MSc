# Some useful points and meetings' notes

Classification Performance
Binary classification has four possible types of results:

True negatives: correctly predicted negatives (zeros)
True positives: correctly predicted positives (ones)
False negatives: incorrectly predicted negatives (zeros)
False positives: incorrectly predicted positives (ones)

---

## 28 July

- CLassification of having the transportation?

- finding the point of interests (where speed = 0)

fix the speed

0. clean the data

1. Create a target variable, a sustainablilty score

2. logistic regression

3. **independent variable:** distance, speed and elevation

4. [0 1] if 1 => cable or not
   3 categories 0 and 1 (cable or sth else)

5. compare the different algorithms (SVM, multi logistic regression ...)

The presentation should be more or less 10 slides:

1. lit review
2. a couple for data
3. a couple for ML algorithm
4. results and conclusion

---

## 15 August

0. ~~Elevation should start from 0.~~

1. ~~Use a boolean variable for wether a lift is used or not (for the entire path)~~

2. Verify the lift

3. Use the speed and distance for x (cum distance, speed and the elevation_diff).
   use that boolean variable as y
4. Summarize the path parameters
