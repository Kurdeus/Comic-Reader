package com.example.reader

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.reader.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    var mData = ArrayList<Comic>()
    lateinit var binding: ActivityMainBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        binding.rvData.layoutManager = LinearLayoutManager(this,LinearLayoutManager.VERTICAL,false)

        mData.add(Comic(0,"https://scans.lastation.us/manga/Kuroiwa-Medaka-ni-Watashi-no-Kawaii-ga-Tsuujinai/0117-006.png"))
        mData.add(Comic(1,"https://scans.lastation.us/manga/Kuroiwa-Medaka-ni-Watashi-no-Kawaii-ga-Tsuujinai/0117-002.png"))
        mData.add(Comic(2,"https://scans.lastation.us/manga/Kuroiwa-Medaka-ni-Watashi-no-Kawaii-ga-Tsuujinai/0117-003.png"))
        mData.add(Comic(3,"https://scans.lastation.us/manga/Kuroiwa-Medaka-ni-Watashi-no-Kawaii-ga-Tsuujinai/0117-005.png"))
        mData.add(Comic(4,"https://scans.lastation.us/manga/Kuroiwa-Medaka-ni-Watashi-no-Kawaii-ga-Tsuujinai/0117-006.png"))
        mData.add(Comic(5,"https://scans.lastation.us/manga/Kuroiwa-Medaka-ni-Watashi-no-Kawaii-ga-Tsuujinai/0117-007.png"))
        mData.add(Comic(6,"https://scans.lastation.us/manga/Kuroiwa-Medaka-ni-Watashi-no-Kawaii-ga-Tsuujinai/0117-008.png"))
        mData.add(Comic(7,"https://scans.lastation.us/manga/Kuroiwa-Medaka-ni-Watashi-no-Kawaii-ga-Tsuujinai/0117-009.png"))
        mData.add(Comic(8,"https://scans.lastation.us/manga/Kuroiwa-Medaka-ni-Watashi-no-Kawaii-ga-Tsuujinai/0117-010.png"))




        val rvAdapter= RvAdapter()

        rvAdapter.differ.submitList(mData)
        binding.rvData.adapter = rvAdapter
    }
}