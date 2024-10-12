package com.latex2nemeth.geom;

public class Box {
	Character [][] box;
	private int width;
	private int height;
	private int baselineHeight;
	
	int index = 0;
	
	public Box(int width, int height, int lineheight) {
		box = new Character [height][width];
		this.width = width;
		this.height = height;
		this.setBaselineHeight(lineheight);
		fillWithSpaces();
	}
	
	public Box(String text) {
		int width = text.length();
		box = new Character[1][width];
		for (int j = 0 ; j < width; j++) {
			box[0][j] = text.charAt(j);
		}
		this.width = width;
		this.height = 1;
		this.setBaselineHeight(0);
	}
			
	protected void fillWithSpaces() {
		for (int i = 0; i < getHeight(); i++) {
			for (int j = 0; j < getWidth(); j++) {
				box[i][j] = ' ';
			}
		}
	}

	public void insert(Box inner, int xpos, int ypos) {
		for (int i = 0; i < inner.getHeight(); i++) {
			for (int j = 0; j < inner.getWidth(); j++) {
				this.box[ypos + i][xpos + j] = inner.box[i][j];
			}
		}
	}
	
	public void insertNext(Box inner) {
		insert(inner, index, 
				this.getBaselineHeight() - inner.getBaselineHeight());
		index = index + inner.getWidth();
	}

	// This is the thing...
	public String toString() {
		StringBuffer buffer = new StringBuffer();
		for (int i = 0 ; i < getHeight(); i++) {
			for (int  j = 0 ; j < getWidth(); j++) {
				buffer.append(box[i][j]);
			}
			if (getHeight()>1)
				buffer.append("\n"); // TODO: Not always!
		}
		return buffer.toString();
	}
	
	public int getWidth() {
		return width;
	}

	public int getHeight() {
		return height;
	}

	String toBraille() {
		return ""; // TODO: FIX
	}

	public void setWidth(int width) {
		this.width = width;
	}

	public void setHeight(int height) {
		this.height = height;
	}

	public int getBaselineHeight() {
		return baselineHeight;
	}

	public void setBaselineHeight(int baselineHeight) {
		this.baselineHeight = baselineHeight;
	}
}
