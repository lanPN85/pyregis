<template>
<div id="info-form">
    <h2><b>Thông tin thí sinh</b></h2>
	<b-form>
		<label for="major">Chọn ngành đăng ký:</label>
		<b-form-select id="major" v-model="selectedMajor" :options="majorOptions"></b-form-select>
		<p></p>

		<label v-if="subjects.length > 0">Điểm thi:</label>
		<b-input-group :left="subj.name" right="/10"
			v-for="subj in subjects" :key="subj.key">
			<b-input type="number" v-model="majorScores[subj.key]" placeholder="Nhập điểm thi"></b-input>
		</b-input-group>
		<p></p>

		<label v-if="selectedSchoolOptions.length > 0">Đánh dấu các trường đã đăng kí: (ít nhất 1 trường)</label>
		<b-form-select multiple v-model="selectedSchools" v-if="selectedSchoolOptions.length > 0"
			:options="selectedSchoolOptions" :select-size="5"></b-form-select>
		<p></p>
	</b-form>

	<b-button block variant="success" :disabled="!scoresFilled || selectedSchools.length <= 0"
		v-on:click="fetchResults">
		Gửi thông tin & Nhận kết quả
	</b-button>

	<div id="loadBar" v-if="isLoading">
		<p class="text-center"><icon name="circle-o-notch" spin></icon> Đang tải</p>
	</div>

	<div id="decision-pane" v-if="decision">
		<p></p>
		<h2><b>Kết quả</b></h2>
		<p>Nên điều chỉnh đăng ký sang các trường sau:</p>
		<b-table :items="decision.schools" :fields="decisionFields">
		</b-table>
	</div>
</div>
</template>

<script>
import 'vue-awesome/icons/circle-o-notch'
import $ from 'jquery'

export default {
	name: 'InfoForm',
	data() {
		return {
			majors: null,
			selectedMajor: null,
			majorScores: {
				math: null, phys: null, chem: null,
				lite: null, eng: null
			},
			selectedSchools: [],
			decision: null,
			decisionFields: {
				name: {label: 'Trường'},
				score_2015: {label: 'Điểm 2015'},
				score_2016: {label: 'Điểm 2016'},
        		cutoff: {label: 'Chỉ tiêu'},
        		notes: {label: 'Ghi chú'}
			},
			isLoading: false
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
      let res = [];
      for (let i=0; i<this.selectedMajor.schools.length; i++) {
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
		},
		fetchResults() {
			this.isLoading = true;
			this.decision = null;
			const component = this;

			let scid = [];
			for (let i=0; i<this.selectedSchools.length; i++) {
				scid.push(this.selectedSchools[i].scid);
			}

				let info = {
				mid: this.selectedMajor.mid,
				scids: scid,
				scores: this.majorScores,
			};

			$.ajax({
				type: 'POST',
				url: '/api/decide',
				dataType: 'json',
				contentType: 'application/json',
				data: JSON.stringify(info),
				success: function (data) {
					setTimeout(function(){
						component.decision = data;
						component.isLoading = false
					}, 500)
				}
			})
		}
	},
	mounted() {
		const component = this;
		$.getJSON('/api/majors/all', function(data){
			component.majors = data;
		});
	}
}
</script>

<style scoped>
#info-form {
	background-color: #f1f1f1;
	min-height: 90vh;
	padding: 10px;
	overflow-y: scroll;
}

#decison-pane {
	margin-top: 10px;
	padding-top: 10px;
}

#loadBar {
	margin-top: 5px;
}
</style>
