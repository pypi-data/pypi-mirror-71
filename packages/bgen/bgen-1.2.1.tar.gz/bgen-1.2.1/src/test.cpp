
#include <chrono>
#include <iostream>
#include <vector>
#include <array>
#include <bitset>

#include "utils.h"

int main() {
  const uint n_samples = 500000;
  int val;
  int offset;
  
  // std::vector<float> sample(3);
  // auto time_0 = std::chrono::high_resolution_clock::now();
  // std::vector<float> empty_vec;
  // auto time_a = std::chrono::high_resolution_clock::now();
  // std::vector<std::vector<float> > nested_vec(n_samples, sample);
  // auto time_b = std::chrono::high_resolution_clock::now();
  // std::vector<float> float_vec(n_samples);
  // auto time_c = std::chrono::high_resolution_clock::now();
  // float nested_float[n_samples][3];
  // auto time_d = std::chrono::high_resolution_clock::now();
  // std::array<std::array<float, 3>, n_samples> nested_array;
  // auto time_e = std::chrono::high_resolution_clock::now();
  float float_array[n_samples * 3];
  // auto time_e_2 = std::chrono::high_resolution_clock::now();
  // std::vector<std::vector<float> > alternate_nested_vec(3, std::vector<float>(n_samples));
  // auto time_f = std::chrono::high_resolution_clock::now();
  // float ** dynamic_nested_float = new float*[3];
  // for (int x=0; x<3; x++) {
  //   dynamic_nested_float[x] = new float[n_samples];
  // }
  // auto time_g = std::chrono::high_resolution_clock::now();
  // float * dynamic_float = new float[3 * n_samples];
  // auto time_h = std::chrono::high_resolution_clock::now();
  //
  // for (int x=0; x < 3; x++ ) {
  //   for (uint y=0; y<n_samples; y++) {
  //     val = dynamic_nested_float[x][y];
  //   }
  // }
  // auto time_i = std::chrono::high_resolution_clock::now();
  //
  // for (uint y=0; y < n_samples; y++ ) {
  //   offset = 3 * y;
  //   for (int x=0; x<3; x++) {
  //     val = dynamic_float[offset + x];
  //   }
  // }
  // auto time_j = std::chrono::high_resolution_clock::now();
  //
  // for (uint y=0; y < n_samples; y++ ) {
  //   offset = 3 * y;
  //   for (int x=0; x<3; x++) {
  //     dynamic_float[offset + x] = x;
  //   }
  // }
  // auto time_k = std::chrono::high_resolution_clock::now();
  //
  // for (int x=0; x < 3; x++ ) {
  //   for (uint y=0; y<n_samples; y++) {
  //     dynamic_nested_float[x][y] = x;
  //   }
  // }
  
  for (int i=0; i < 5000; i++) {
    // auto time_l = std::chrono::high_resolution_clock::now();
    //
    // for (uint offset=0; offset < n_samples * 3; offset += 3 ) {
    //   for (int x=0; x < 3; x++ ) {
    //     val = float_array[offset + x];
    //   }
    // }
    auto time_m = std::chrono::high_resolution_clock::now();
    // std::cout << i << " - access float array: " << std::chrono::duration_cast<std::chrono::microseconds>(time_m - time_l).count() << std::endl;
    
    for (uint offset=0; offset < n_samples * 3; offset += 3 ) {
      for (int x=0; x < 3; x++ ) {
        float_array[offset + x] = x;
      }
    }
    // for (uint offset=0; offset < n_samples * 3; offset++ ) {
    //     float_array[offset] = 5.0;
    // }
    
    auto time_n = std::chrono::high_resolution_clock::now();
    std::cout << i << "\t" << std::chrono::duration_cast<std::chrono::microseconds>(time_n - time_m).count() << "\n";
  }
  
  
  // std::cout << " - construct empty vector: " << std::chrono::duration_cast<std::chrono::microseconds>(time_a - time_0).count() << std::endl;
  // std::cout << " - construct nested vector: " << std::chrono::duration_cast<std::chrono::microseconds>(time_b - time_a).count() << std::endl;
  // std::cout << " - construct float vector " << std::chrono::duration_cast<std::chrono::microseconds>(time_c - time_b).count() << std::endl;
  // std::cout << " - construct nested float: " << std::chrono::duration_cast<std::chrono::microseconds>(time_d - time_c).count() << std::endl;
  // std::cout << " - construct nested array: " << std::chrono::duration_cast<std::chrono::microseconds>(time_e - time_d).count() << std::endl;
  // std::cout << " - construct float array: " << std::chrono::duration_cast<std::chrono::microseconds>(time_e_2 - time_e).count() << std::endl;
  // std::cout << " - construct alternate nested vector: " << std::chrono::duration_cast<std::chrono::microseconds>(time_f - time_e_2).count() << std::endl;
  // std::cout << " - construct dynamic nested float: " << std::chrono::duration_cast<std::chrono::microseconds>(time_g - time_f).count() << std::endl;
  // std::cout << " - construct dynamic float: " << std::chrono::duration_cast<std::chrono::microseconds>(time_h - time_g).count() << std::endl;
  // std::cout << " - access dynamic nested float: " << std::chrono::duration_cast<std::chrono::microseconds>(time_i - time_h).count() << std::endl;
  // std::cout << " - access dynamic float: " << std::chrono::duration_cast<std::chrono::microseconds>(time_j - time_i).count() << std::endl;
  // std::cout << " - set dynamic nested float: " << std::chrono::duration_cast<std::chrono::microseconds>(time_l - time_k).count() << std::endl;
  // std::cout << " - set dynamic float: " << std::chrono::duration_cast<std::chrono::microseconds>(time_k - time_j).count() << std::endl;
  // std::cout << " - access float array: " << std::chrono::duration_cast<std::chrono::microseconds>(time_m - time_l).count() << std::endl;
  // std::cout << " - set float array: " << std::chrono::duration_cast<std::chrono::microseconds>(time_n - time_m).count() << std::endl;
  
}

// gcc -lstdc++ -std=c++11 test.cpp utils.cpp
