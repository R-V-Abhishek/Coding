package com.example.program1

import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        Toast.makeText(this, "Toast onCreate", Toast.LENGTH_LONG).show()
        Log.d("activity", "onCreate")
    }

    override fun onStart() {
        super.onStart()
        Toast.makeText(this, "Toast onStart", Toast.LENGTH_LONG).show()
        Log.d("activity", "onStart")
    }

    override fun onResume() {
        super.onResume()
        Toast.makeText(this, "Toast onResume", Toast.LENGTH_LONG).show()
        Log.d("activity", "onResume")
    }

    override fun onPause() {
        super.onPause()
        Toast.makeText(this, "Toast onPause", Toast.LENGTH_LONG).show()
        Log.d("activity", "onPause")
    }

    override fun onStop() {
        super.onStop()
        Toast.makeText(this, "Toast onStop", Toast.LENGTH_LONG).show()
        Log.d("activity", "onStop")
    }

    override fun onDestroy() {
        super.onDestroy()
        Toast.makeText(this, "Toast onDestroy", Toast.LENGTH_LONG).show()
        Log.d("activity", "onDestroy")
    }

    override fun onRestart() {
        super.onRestart()
        Toast.makeText(this, "Toast onRestart", Toast.LENGTH_LONG).show()
        Log.d("activity", "onRestart")
    }
}