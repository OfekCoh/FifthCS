import cv2
import numpy as np
import os
import shutil
import sys

#matches is of (3|4 X 2 X 2) size. Each row is a match - pair of (kp1,kp2) where kpi = (x,y)
def get_transform(matches, is_affine):
	src_points, dst_points = matches[:,0], matches[:,1]
	
	# Add your code here
	if is_affine:
		T,_=cv2.estimateAffine2D(src_points,dst_points) #(2X3)
	else:
		T,_=cv2.findHomography(src_points,dst_points) #(3X3)

	return T  # T is used for forward mapping


def stitch(img1, img2):
	stitched_image = np.where(img2>img1, img2, img1) # take the max value from (img1,img2)
	return stitched_image


# Output size is (w,h)
def inverse_transform_target_image(target_img, original_transform, output_size):

	is_affine = original_transform.shape == (2, 3) # check if affine or not

	if is_affine:  # if the transform is affine (2x3) convert it to homography matrix (3x3)
		homography_transform = np.vstack([original_transform, [0, 0, 1]])
	else: # transform is homography so already (3x3)
		homography_transform = original_transform

	inverse_transform = np.linalg.inv(homography_transform)  # compute the inverse transformation
	
	if is_affine:
		inverse_transform = inverse_transform[:2, :] # if the original was affine, return back to 2x3 shape
		transformed_img = cv2.warpAffine(target_img, inverse_transform, output_size, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) # Perform the inverse warp- affine

	else: 
		transformed_img = cv2.warpPerspective(target_img, inverse_transform, output_size, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) # Perform the inverse warp

	return transformed_img


# returns list of pieces file names
def prepare_puzzle(puzzle_dir):
	edited = os.path.join(puzzle_dir, 'abs_pieces')
	if os.path.exists(edited):
		shutil.rmtree(edited)
	os.mkdir(edited)
	
	affine = 4 - int("affine" in puzzle_dir)
	
	matches_data = os.path.join(puzzle_dir, 'matches.txt')
	n_images = len(os.listdir(os.path.join(puzzle_dir, 'pieces')))

	matches = np.loadtxt(matches_data, dtype=np.int64).reshape(n_images-1,affine,2,2)
	
	return matches, affine == 3, n_images


if __name__ == '__main__':
	lst = ['puzzle_affine_1', 'puzzle_affine_2', 'puzzle_homography_1']
	# lst = ['puzzle_affine_1']

	for puzzle_dir in lst:
		print(f'Starting {puzzle_dir}')
		puzzle = os.path.join('puzzles', puzzle_dir)   # creates the path puzzles/puzzle_affine_1
		pieces_pth = os.path.join(puzzle, 'pieces')
		edited = os.path.join(puzzle, 'abs_pieces')   # creates the path puzzles/abs_pieces
		matches, is_affine, n_images = prepare_puzzle(puzzle)
		
		# Add your code here
		first_image = cv2.imread(os.path.join(pieces_pth, 'piece_1.jpg'))
		canvas_size = (first_image.shape[1], first_image.shape[0])  # (width, height)
		final_puzzle = np.zeros((canvas_size[1], canvas_size[0], 3), dtype=np.uint8)  # Blank canvas

		aligned_piece_path = os.path.join(edited, f'piece_1_relative.jpg') # creates the path puzzles/abs_pieces/piece_1_relative.jpg
		cv2.imwrite(aligned_piece_path, first_image) # save the first piece in the abs_pieces folder

		# place the first image on the canvas
		final_puzzle[:canvas_size[1], :canvas_size[0]] = first_image
		
		# continure with all other pieces
		for idx in range(1,n_images):
			piece = cv2.imread(os.path.join(pieces_pth, f'piece_{idx+1}.jpg'))
			
			M = get_transform(matches=matches[idx-1], is_affine=is_affine) 
			M = M.astype(np.float32)
			
			aligned_piece = inverse_transform_target_image(piece, M, canvas_size) # get the aligned piece

			aligned_piece_path = os.path.join(edited, f'piece_{idx+1}_relative.jpg') # creates the path puzzles/abs_pieces/piece_2_relative.jpg
			cv2.imwrite(aligned_piece_path, aligned_piece) # save the piece in the abs_pieces folder

			final_puzzle = stitch(final_puzzle, aligned_piece) # stitch the aligned piece to the canvas
			
		cv2.imshow("image", final_puzzle)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	
		sol_file = f'solution.jpg'
		cv2.imwrite(os.path.join(puzzle, sol_file), final_puzzle)



