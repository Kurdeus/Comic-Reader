package com.example.reader

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.AsyncListDiffer
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.RecyclerView
import com.example.reader.databinding.FragmentComicPageBinding
import com.google.android.material.snackbar.Snackbar
import com.squareup.picasso.Callback
import com.squareup.picasso.Picasso
import java.lang.Exception

class RvAdapter : RecyclerView.Adapter<RvAdapter.ViewHolder>() {
    lateinit var binding: FragmentComicPageBinding
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        binding =
            FragmentComicPageBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.setData(differ.currentList[position])


    }

    override fun getItemCount() = differ.currentList.size


    inner class ViewHolder(val binder: FragmentComicPageBinding) : RecyclerView.ViewHolder(binder.root) {
        fun setData(item: Comic) {

            binder.apply {
                val response = Picasso.get().load(item.comicUrl)




                response.placeholder(R.color.black)
                    .into(ivComic, object : Callback {

                        override fun onSuccess() {
                            progressBar.visibility = View.GONE
                        }

                        override fun onError(e: Exception?) {
                            Snackbar.make(ivComic, "error", Snackbar.LENGTH_SHORT).show()
                        }
                    })
            }
        }


    }

    private val diffCallback = object : DiffUtil.ItemCallback<Comic>() {
        override fun areItemsTheSame(oldItem: Comic, newItem: Comic): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: Comic, newItem: Comic): Boolean {
            return oldItem == newItem
        }
    }

    val differ = AsyncListDiffer(this, diffCallback)
}
