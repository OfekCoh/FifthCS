sk = (img2 > 0).astype(np.uint8)
	stitched_image = np.where(mask, img2, img1)
	return stitched_image