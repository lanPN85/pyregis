<template>
<div id="info-form">
    <h2>Thông tin thí sinh</h2>
	<b-form>
		<label for="major">Chọn ngành đăng ký:</label>
		<b-form-select id="major" v-model="selectedMajor" :options="majorOptions"></b-form-select>
		<p></p>
		
		<label>Điểm thi:</label>
		<b-input-group :left="subj.name" right="/10"
			v-for="subj in subjects" :key="subj.key">
			<b-input type="number" v-model="majorScores[subj.key]" placeholder="Nhập điểm thi"></b-input>
		</b-input-group>
		<p></p>

		<label>Đánh dấu các trường đã đăng kí:</label>
		<b-form-select multiple v-model="selectedSchools" 
			:options="selectedSchoolOptions" :select-size="5"></b-form-select>
		<p></p>	
	</b-form>
	
	<b-button block variant="success" :disabled="!scoresFilled">Gửi thông tin & Nhận kết quả</b-button>

	<div v-if="resultSchools">

	</div>
</div>
</template>

<script>
export default {
	name: 'InfoForm',
	data() {
		return {
			majors: [
				{name: 'A', group: 'D', schools: [{scid: 1, name: 'DHBKHN'}]}, 
				{name: 'B', group: 'A', schools: [{scid: 2, name: 'DHQG'}]}
			],
			selectedMajor: null,
			majorScores: {
				math: null, phys: null, chem: null,
				lite: null, eng: null
			},
			selectedSchools: [],
			resultSchools: null
		}
	},
	computed: {
		majorOptions() {
			if (!this.majors) return null;
			var res = [];
			for (var i=0; i<this.majors.length; i++) {
				res.push({text: this.majors[i].name, value: this.majors[i]});
			}
			return res;
		},
		selectedSchoolOptions() {
			if (!this.selectedMajor) return [];
			var res = [];
			for (var i=0; i<this.selectedMajor.schools.length; i++) {
				res.push({text: this.selectedMajor.schools[i].name, value: this.selectedMajor.schools[i]});
			}
			return res;
		},
		subjects() {
			if (!this.selectedMajor) return [];
			if (this.selectedMajor.group === 'A') {
				return [
					{name: 'Toán', key: 'math',},
					{name: 'Vật lý', key: 'phys'},
					{name: 'Hóa học', key: 'chem'}
				]
			} else if (this.selectedMajor.group === 'D') {
				return [
					{name: 'Toán', key: 'math',},
					{name: 'Ngữ văn', key: 'lite'},
					{name: 'Tiếng Anh', key: 'eng'}
				]
			} else return [];
		},
		scoresFilled() {
			if (!this.selectedMajor) return false;
			if (this.selectedMajor.group === 'A') {
				return this.majorScores.phys && this.isValidScore(this.majorScores.phys) &&
					this.majorScores.math && this.isValidScore(this.majorScores.math) &&
					this.majorScores.chem && this.isValidScore(this.majorScores.chem)
			} else if (this.selectedMajor.group === 'D') {
				return this.majorScores.lite && this.isValidScore(this.majorScores.lite) &&
					this.majorScores.math && this.isValidScore(this.majorScores.math) &&
					this.majorScores.eng && this.isValidScore(this.majorScores.eng)
			} else return false;
		}
	},
	methods: {
		isValidScore(score) {
			return score >= 0 && score <= 10;
		}
	}
}
</script>

<style scoped>
#info-form {
	background-color: #f1f1f1;
	min-height: 90vh;
	padding: 10px;
}
</style>
