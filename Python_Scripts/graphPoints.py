import matplotlib.pyplot as plt
plt.plot([1,2,3,4, 5, 6], [5.15385,10.1987,29.97827,77.11243,161.0987, 464.6425], 'ro')

eb = plt.errorbar(1, 5.15385, yerr=1.39489, fmt='', color='b')
eb = plt.errorbar(2, 10.1987, yerr=3.13897, fmt='', color='b')
eb = plt.errorbar(3, 29.97827, yerr=8.65322, fmt='', color='b')
eb = plt.errorbar(4, 77.11243, yerr=18.70535, fmt='', color='b')
eb = plt.errorbar(5, 161.0987, yerr=28.22994, fmt='', color='b')
eb = plt.errorbar(6, 464.6425, yerr=26.25558, fmt='', color='b')
plt.axis([0, 7, 0, 500])
plt.title('Mean response time per load since restart')
plt.xlabel("Number of times website loaded since restart")
plt.ylabel("Seconds for the webpage to load")
plt.show()