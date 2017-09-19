#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>

#include <iostream>
#include <vector>
#include <algorithm>

using std::vector;

struct Bucket {
    int timestamp;
    int flag; // use to indicate timezone
    Bucket (int timestamp = 0, int flag = 1) :
        timestamp(timestamp), flag(flag) {}
	int getTime(int otherFlag, int N) {
		// if the flag is different, shift one timezone
		return flag == otherFlag ? timestamp : timestamp - N;
	}
};

class BitStream {
private:
    FILE* f;
public:
    BitStream() {
        f = NULL;
    }
    BitStream (const char* filename) {
        if (!(f = fopen(filename, "r"))) {
            printf("Cannot open file %s\n", filename);
            exit(-1);
        }
    }
    int getNext() {
        if (!feof(f)) {
            return fgetc(f) - 48;
        } else {
            printf("Reach the end!\n");
            exit(-1);
        }
    }
    bool hasNext() {
        return !feof(f);
    }
    void done() {
        if (f != NULL) {
            fclose(f);
            f = NULL;
        }
    }
    ~BitStream() {
        if (f != NULL) {
            done();
        }
    }
};

template <int N = 1000, int r = 2>
class DGIMCounter {
private:
    vector<vector<Bucket> > buckets;
    BitStream *bitStream;
    // how many buckets do we need?
    int bucketNum = ceil(log2(N / (r - 1) + 1));
    // current time (1 - N)
    int currentTime = 0; // invalid time
    // left most bucket position
    int leftMostBucket = 0;
	// flag
	int flag = -1;

    // when one bit comes in, update bucket data
    void updateBuckets() {
        int currentBit = bitStream->getNext();
        if (currentBit != 0 && currentBit != 1)
            return ;
        // update time
        currentTime = currentTime == N - 1 ? N : (currentTime + 1) % N;
		if (currentTime == 1) this->flag = 0 - this->flag;
        // check the leftmost bucket
        // is it outdated ?
        if (!buckets[leftMostBucket].empty() &&
                buckets[leftMostBucket][0].getTime(this->flag, N) <= currentTime - N)
            buckets[leftMostBucket].erase(buckets[leftMostBucket].begin());
        // update leftmost position
        if (leftMostBucket != 0 && buckets[leftMostBucket].empty())
            --leftMostBucket;
        // if current bit is '1'
        if (currentBit == 1) {
            buckets[0].push_back(Bucket(currentTime, this->flag));
            mergeBuckets();
        }
    }
    void mergeBuckets() {
        for (int i = 0; i < bucketNum; ++i) {
            // update leftmost position
            if (!buckets[i].empty())
                leftMostBucket = std::max(leftMostBucket, i);
            if (buckets[i].size() <= r) break;
            Bucket tmp = buckets[i][1];
            // erase the first and the second bucket
            buckets[i].erase(buckets[i].begin(), buckets[i].begin() + 2);
            if (i < bucketNum - 1) {
                buckets[i + 1].push_back(tmp);
            }
        }
    }
public:
    DGIMCounter (BitStream *bitStream) {
        buckets.resize(bucketNum);
        // initialize time
        currentTime = 0;
        // leftmost bucket position
        leftMostBucket = 0;
		// flag
		flag = -1;
        this->bitStream = bitStream;
    }
    void start() {
        // read stream data
        while (bitStream->hasNext()) {
            updateBuckets();
        }
        // finish
        bitStream->done();
    }
    // query number of '1' bits
    int query (int k) {
        double count = 0;
        int coverage = -1;
        int lastPart = 0;
        int endTime = currentTime - k + 1;
        int i = 0, j = 0;
        for (; i <= leftMostBucket; ++i) {
            for (j = 0; j < buckets[i].size(); ++j) {
                if (buckets[i][j].getTime(flag, N)  >= endTime) {
                    coverage = buckets[i][j].timestamp - endTime + 1;
                    lastPart = 1 << i;
                    count += lastPart;
                }
                else break;
            }
        }
        if (endTime <= 0) return count;
        // optimize
        count -= lastPart;
        int halfOneBits = ceil(lastPart / 2.0);
        if (coverage < halfOneBits)
            return count + coverage; // upperBound
        else return count + halfOneBits;
    }
    void print() {
        printf("Buckets info.:\n");
        for (int i = 0; i < buckets.size(); ++i) {
            if (!buckets[i].empty())
                printf("size = %d\nt = ", i);
            for (int j = 0; j < buckets[i].size(); ++j) {
                printf("%d\t", buckets[i][j].getTime(this->flag, N));
            }
            std::cout<<"\n";
        }
    }
};

// how to compile? g++ DGIM.cpp -o DGIM -std=c++11 -O3
// how to run? ./DGIM stream_file
// which platform: linux
int main(int argc, char** argv) {
    if (argc <  2) {
        printf("Usage: %s filename\n", argv[0]);
        exit(-1);
    }
    const char* filename = argv[1];
    int k = 1000;
    BitStream bitStream(filename);
    DGIMCounter<1000, 2> dgimCounter = DGIMCounter<1000, 2>(&bitStream);
    dgimCounter.start();
    dgimCounter.print();
    printf("Query result = %d\n", dgimCounter.query(k));
    return 0;
}

